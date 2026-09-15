#!/usr/bin/env python3
"""Pack files into a prompt and ask DeepSeek. Stdlib only."""

import argparse
import datetime
import fnmatch
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

API_URL = "https://api.deepseek.com/chat/completions"
ENV_FILE = Path.home() / ".claude" / ".env"
KEY_FILE = Path.home() / ".claude" / "deepseek_key"
USAGE_FILE = Path.home() / ".claude" / ".deepseek_usage.json"
PLACEHOLDER = "hier-key-einfuegen"

# Hard cap on API calls per calendar day. Raise it only in .env
# (DEEPSEEK_DAILY_LIMIT=...) -- deliberately not a CLI flag, so it cannot be
# waved away mid-session by the agent that is spending the budget.
DEFAULT_DAILY_LIMIT = 50

SKIP_DIRS = {
    ".git", "node_modules", "dist", "build", ".next", "out", "target",
    "venv", ".venv", "__pycache__", ".pytest_cache", ".mypy_cache",
    "vendor", "Pods", ".gradle", "coverage", ".turbo", ".cache",
}
SKIP_FILES = {"*.lock", "*.min.js", "*.map", "package-lock.json", "yarn.lock", "pnpm-lock.yaml"}

# Never leave the machine unless explicitly named on the command line.
SECRET_FILES = {
    ".env", ".env.*", "*.pem", "*.key", "*.p12", "*.pfx", "id_rsa*", "id_ed25519*",
    "*credentials*.json", "*service-account*.json", "*.keystore", ".netrc", ".npmrc",
}
# Substrings that suggest a real secret sits in the content.
SECRET_MARKERS = (
    "-----BEGIN", "sk-ant-", "sk-proj-", "AKIA", "ghp_", "github_pat_",
    "xoxb-", "private_key", "client_secret",
)
BINARY_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip", ".gz",
    ".tar", ".mp4", ".mov", ".mp3", ".woff", ".woff2", ".ttf", ".eot",
    ".so", ".dylib", ".dll", ".exe", ".bin", ".db", ".sqlite", ".pyc",
}

# Code is roughly 3 characters per token. Deliberately conservative.
CHARS_PER_TOKEN = 3


def die(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def read_env_file(path: Path):
    """Minimal KEY=VALUE parser. No export, no interpolation, no multiline."""
    values = {}
    if not path.exists():
        return values
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        values[k.strip()] = v.strip().strip("'\"")
    return values


def find_env_files():
    """Project .env first, walking up to the home dir, then the global one."""
    found = []
    cwd = Path.cwd().resolve()
    home = Path.home().resolve()
    for d in [cwd, *cwd.parents]:
        candidate = d / ".env"
        if candidate.is_file():
            found.append(candidate)
        if d == home:
            break
    if ENV_FILE.is_file() and ENV_FILE not in found:
        found.append(ENV_FILE)
    return found


def get_limit():
    raw = os.environ.get("DEEPSEEK_DAILY_LIMIT", "").strip()
    if not raw:
        for env_path in find_env_files():
            raw = read_env_file(env_path).get("DEEPSEEK_DAILY_LIMIT", "").strip()
            if raw:
                break
    if not raw:
        return DEFAULT_DAILY_LIMIT
    try:
        return max(1, int(raw))
    except ValueError:
        print(f"[!] DEEPSEEK_DAILY_LIMIT={raw!r} is not a number, "
              f"using {DEFAULT_DAILY_LIMIT}", file=sys.stderr)
        return DEFAULT_DAILY_LIMIT


def get_key():
    """Env var wins, then the nearest .env walking up, then the legacy key file."""
    key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    source = "$DEEPSEEK_API_KEY"
    checked = []

    for env_path in find_env_files():
        if key:
            break
        checked.append(env_path)
        key = read_env_file(env_path).get("DEEPSEEK_API_KEY", "").strip()
        source = str(env_path)

    if not key and KEY_FILE.exists():
        key = KEY_FILE.read_text().strip()
        source = str(KEY_FILE)

    if key == PLACEHOLDER:
        die(f"{source} still has the placeholder in it.\n"
            f"  Replace '{PLACEHOLDER}' with your real key.")
    if not key:
        looked = "\n".join(f"    {p}" for p in checked) or "    (no .env found)"
        die(f"no API key. Put DEEPSEEK_API_KEY=sk-... in a .env next to your project,\n"
            f"  or in {ENV_FILE}. Looked in:\n{looked}\n"
            f"  (get one at https://platform.deepseek.com/api_keys)")
    if not key.startswith("sk-"):
        print(f"[!] key does not start with 'sk-' — probably wrong value", file=sys.stderr)
    return key


def matches_any(path: Path, patterns) -> bool:
    return any(
        fnmatch.fnmatch(path.name, pat) or fnmatch.fnmatch(str(path), pat)
        for pat in patterns
    )


def today() -> str:
    return datetime.date.today().isoformat()


def read_usage():
    """Calls made today. Resets automatically on a new calendar day."""
    try:
        data = json.loads(USAGE_FILE.read_text())
    except (OSError, json.JSONDecodeError):
        return 0
    if data.get("date") != today():
        return 0
    return int(data.get("count", 0))


def bump_usage():
    count = read_usage() + 1
    try:
        USAGE_FILE.write_text(json.dumps({"date": today(), "count": count}))
    except OSError as e:
        print(f"[!] could not record usage: {e}", file=sys.stderr)
    return count


def check_budget(limit):
    used = read_usage()
    if used >= limit:
        die(f"daily limit reached: {used}/{limit} calls today.\n"
            f"  Resets at midnight. Raise DEEPSEEK_DAILY_LIMIT in your .env "
            f"if you really need more.\n"
            f"  Answer the question from the local codebase instead.")
    return used


def should_skip(path: Path, excludes) -> bool:
    if any(part in SKIP_DIRS for part in path.parts):
        return True
    if path.suffix.lower() in BINARY_EXT:
        return True
    return matches_any(path, list(SKIP_FILES) + list(excludes))


def split_range(pattern):
    """'src/a.ts:10-40' -> (Path('src/a.ts'), (10, 40)). Otherwise (path, None).

    Only treats a trailing ':N-M' as a range when the remaining path is a real
    file -- directory names containing a colon (e.g. '24:7 on/') stay intact.
    """
    m = re.match(r"^(.*):(\d+)-(\d+)$", pattern)
    if not m:
        return Path(pattern), None
    base, start, end = m.group(1), int(m.group(2)), int(m.group(3))
    if not Path(base).is_file():
        return Path(pattern), None
    if start < 1 or end < start:
        die(f"bad line range in {pattern!r}: start must be >=1 and <= end")
    return Path(base), (start, end)


def collect(patterns, excludes):
    """Expand paths/globs into a deduped, ordered list of readable text files.

    Secret-looking files are dropped when they arrive via a glob, but kept when
    the user names the exact path -- that is an explicit decision to send it.
    Returns (files, ranges, secrets) where ranges maps a path to (start, end).
    """
    out, seen, secrets, ranges = [], set(), [], {}
    for pat in patterns:
        p, line_range = split_range(pat)
        explicit = p.is_file()
        if p.is_dir():
            matches = sorted(x for x in p.rglob("*") if x.is_file())
        elif explicit:
            matches = [p]
            if line_range:
                ranges[p] = line_range
        else:
            matches = sorted(Path().glob(pat))
        for m in matches:
            if not m.is_file() or should_skip(m, excludes):
                continue
            if not explicit and matches_any(m, SECRET_FILES):
                secrets.append(m)
                continue
            r = m.resolve()
            if r in seen:
                continue
            seen.add(r)
            out.append(m)
    return out, ranges, secrets


def slice_lines(content, line_range):
    if not line_range:
        return content, None
    start, end = line_range
    lines = content.splitlines()
    if start > len(lines):
        die(f"line range {start}-{end} starts past the end of the file "
            f"({len(lines)} lines)")
    return "\n".join(lines[start - 1:end]), (start, min(end, len(lines)))


def scan_secrets(files):
    """Files whose content looks like it holds a live credential."""
    hits = []
    for f in files:
        content = read_text(f)
        if content and any(m in content for m in SECRET_MARKERS):
            hits.append(f)
    return hits


def read_text(path: Path):
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def git_diff(ref):
    cmd = ["git", "diff"] + ([ref] if ref else [])
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError) as e:
        die(f"git diff failed: {e}")
    if r.returncode != 0:
        die(f"git diff failed: {r.stderr.strip()}")
    return r.stdout


def build_context(files, ranges, diff_text, budget_tokens):
    """Assemble the file blob, stopping once the budget is spent.

    Returns (context, included, skipped, tokens, sizes) where sizes maps each
    included path to its token count -- that is what makes pruning actionable.
    """
    budget_chars = budget_tokens * CHARS_PER_TOKEN
    parts, included, skipped, sizes, used = [], [], [], {}, 0

    if diff_text:
        block = f"=== GIT DIFF ===\n{diff_text}\n"
        parts.append(block)
        used += len(block)
        sizes[Path("<git diff>")] = len(block) // CHARS_PER_TOKEN

    for f in files:
        content = read_text(f)
        if content is None:
            continue
        content, applied = slice_lines(content, ranges.get(f))
        if applied:
            label = f"{f} (lines {applied[0]}-{applied[1]})"
        else:
            label = f"{f} ({content.count(chr(10)) + 1} lines)"
        block = f"\n=== FILE: {label} ===\n{content}\n"
        if used + len(block) > budget_chars:
            skipped.append(f)
            continue
        parts.append(block)
        used += len(block)
        included.append(f)
        sizes[f] = len(block) // CHARS_PER_TOKEN

    return "".join(parts), included, skipped, used // CHARS_PER_TOKEN, sizes


def call_api(key, model, system, user, temperature, stream, timeout):
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "stream": stream,
    }
    # deepseek-reasoner rejects temperature; only send it for chat models.
    if not model.endswith("reasoner"):
        body["temperature"] = temperature

    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
            "Accept": "text/event-stream" if stream else "application/json",
        },
        method="POST",
    )

    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        # Accepted by the API, so it is billed -- count it even if the stream
        # dies below, otherwise a crash loop would spend the budget for free.
        bump_usage()
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:500]
        hint = ""
        if e.code == 401:
            hint = "\n  -> key rejected. Check DEEPSEEK_API_KEY."
        elif e.code == 402:
            hint = "\n  -> account out of credit. Top up at platform.deepseek.com."
        elif e.code == 429:
            hint = "\n  -> rate limited. Wait and retry."
        die(f"HTTP {e.code}: {detail}{hint}")
    except urllib.error.URLError as e:
        die(f"connection failed: {e.reason}")

    if not stream:
        data = json.loads(resp.read())
        msg = data["choices"][0]["message"]
        reasoning = msg.get("reasoning_content")
        if reasoning:
            print("--- reasoning ---", file=sys.stderr)
            print(reasoning, file=sys.stderr)
            print("--- answer ---", file=sys.stderr)
        print(msg["content"])
        return data.get("usage", {})

    usage = {}
    in_reasoning = False
    for raw in resp:
        line = raw.decode(errors="replace").strip()
        if not line.startswith("data: "):
            continue
        payload = line[6:]
        if payload == "[DONE]":
            break
        try:
            chunk = json.loads(payload)
        except json.JSONDecodeError:
            continue
        if chunk.get("usage"):
            usage = chunk["usage"]
        choices = chunk.get("choices")
        if not choices:
            continue
        delta = choices[0].get("delta", {})
        # reasoner streams its chain of thought first, on a separate field
        if delta.get("reasoning_content"):
            if not in_reasoning:
                print("--- reasoning ---", file=sys.stderr, flush=True)
                in_reasoning = True
            sys.stderr.write(delta["reasoning_content"])
            sys.stderr.flush()
        if delta.get("content"):
            if in_reasoning:
                print("\n--- answer ---", file=sys.stderr, flush=True)
                in_reasoning = False
            sys.stdout.write(delta["content"])
            sys.stdout.flush()
    print()
    return usage


SYSTEM = (
    "You are a senior engineer reviewing code for another AI agent (Claude Code) "
    "that will act on your answer. Be concrete and specific: name files, functions "
    "and line references from the provided context. Prefer precise findings over "
    "general advice. If the context is insufficient to answer, say exactly what is "
    "missing instead of guessing."
)


def main():
    ap = argparse.ArgumentParser(
        description="Ask DeepSeek about a pile of code.",
        epilog="example: ask_deepseek.py 'where is the race condition?' -f 'src/**/*.ts'",
    )
    ap.add_argument("question", nargs="?", help="the question (or pipe it via stdin)")
    ap.add_argument("-f", "--files", action="append", default=[], metavar="GLOB",
                    help="file, directory or glob; repeatable")
    ap.add_argument("-x", "--exclude", action="append", default=[], metavar="GLOB",
                    help="exclude pattern; repeatable")
    ap.add_argument("-d", "--diff", nargs="?", const="", metavar="REF",
                    help="include `git diff [REF]`")
    ap.add_argument("-m", "--model", default="deepseek-chat",
                    help="deepseek-chat (fast, default) or deepseek-reasoner (deep)")
    ap.add_argument("-b", "--budget", type=int, default=50000, metavar="TOKENS",
                    help="max context tokens to pack (default 50000)")
    ap.add_argument("-t", "--temperature", type=float, default=0.0)
    ap.add_argument("--timeout", type=int, default=600, help="seconds (default 600)")
    ap.add_argument("--no-stream", action="store_true")
    ap.add_argument("--dry-run", action="store_true",
                    help="show what would be sent, don't call the API")
    ap.add_argument("--allow-secrets", action="store_true",
                    help="send files even if they look like they contain credentials")
    args = ap.parse_args()

    question = args.question
    if not question and not sys.stdin.isatty():
        question = sys.stdin.read().strip()
    if not question:
        die("no question given")

    files, ranges, secret_files = (collect(args.files, args.exclude)
                                   if args.files else ([], {}, []))
    diff_text = git_diff(args.diff) if args.diff is not None else ""

    if not files and not diff_text:
        die("no context: pass -f/--files and/or -d/--diff")

    if secret_files:
        print(f"[!] skipped {len(secret_files)} secret-looking file(s): "
              f"{', '.join(str(s) for s in secret_files[:3])}", file=sys.stderr)
        print("[!] name the path explicitly if you really want to send them", file=sys.stderr)

    flagged = scan_secrets(files)
    if flagged and not args.allow_secrets:
        print("\n[!] STOP: these files contain what looks like a live credential:", file=sys.stderr)
        for f in flagged:
            print(f"      {f}", file=sys.stderr)
        die("refusing to send. Rotate/remove the secret, exclude the file with -x, "
            "or pass --allow-secrets if it is a false positive.")

    context, included, skipped, tokens, sizes = build_context(
        files, ranges, diff_text, args.budget)
    limit = get_limit()

    print(f"[{len(included)} files, ~{tokens:,} tokens, model={args.model}, "
          f"{read_usage()}/{limit} calls today]", file=sys.stderr)
    if tokens < 15000 and not args.dry_run:
        print(f"[!] only ~{tokens:,} tokens — that fits in your own context. "
              f"Read the files directly instead of spending a call.", file=sys.stderr)
    if skipped:
        print(f"[!] {len(skipped)} files dropped, budget full: "
              f"{', '.join(str(s) for s in skipped[:5])}"
              f"{' ...' if len(skipped) > 5 else ''}", file=sys.stderr)
        print("[!] raise --budget or narrow --files", file=sys.stderr)

    user = f"{context}\n\n=== QUESTION ===\n{question}\n"

    if args.dry_run:
        print("\n  would send (biggest first — prune the fat ones):", file=sys.stderr)
        for f, n in sorted(sizes.items(), key=lambda kv: -kv[1]):
            share = (n * 100 // tokens) if tokens else 0
            note = f" [lines {ranges[f][0]}-{ranges[f][1]}]" if f in ranges else ""
            print(f"    {n:>7,} tok  {share:>2}%  {f}{note}", file=sys.stderr)
        print(f"\n[dry run] ~{tokens:,} context tokens, nothing sent. "
              f"{limit - read_usage()} of {limit} calls left today.", file=sys.stderr)
        return

    check_budget(limit)
    key = get_key()
    usage = call_api(key, args.model, SYSTEM, user, args.temperature,
                     not args.no_stream, args.timeout)
    if usage:
        hit = usage.get("prompt_cache_hit_tokens", 0)
        print(f"\n[in={usage.get('prompt_tokens', 0):,} "
              f"(cached {hit:,}) out={usage.get('completion_tokens', 0):,} | "
              f"{read_usage()}/{limit} calls today]", file=sys.stderr)


if __name__ == "__main__":
    main()
