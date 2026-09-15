---
name: ask-deepseek
description: Last resort for code questions that do not fit in the local context — offloads a large pile of code to DeepSeek's external API in one call. Use ONLY when the code needed to answer would blow up your own context (repo-wide audits across dozens of files, a huge diff, "where is X used everywhere"), or when the user explicitly asks ("/deepseek", "frag deepseek", "zweite meinung", "lass deepseek draufschauen"). Do NOT use for questions you can answer by reading the files yourself — that is almost always the better answer, and calls are hard-capped at 50 per day.
---

# Ask DeepSeek

Offload a code question to DeepSeek's API. The point: DeepSeek reads a large pile of code in **one** call and hands back a compact answer, so your context absorbs the conclusion instead of the raw files.

## When NOT to use this

This is the expensive, worse-informed path. It is **not** a general "ask a second model" button. Default to reading the code yourself; reach for this only when you genuinely cannot.

Skip it and read the files yourself when:

- The context fits. Under ~15k tokens is not "too much" — that is a normal read. The script warns you when you're below that line; listen to it.
- Fewer than roughly 5–10 files, or you already know which file is at fault.
- The question needs running, testing, or editing anything. DeepSeek can't. You can.
- It's a follow-up answerable from files you already read this session.
- The answer must be exactly right. DeepSeek sees a slice, has no history, can't verify — you're better on this repo than it is.

Reach for it when:

- Answering honestly requires reading more code at once than you can hold — repo-wide sweeps, "every call site of X across 60 files", a 3000-line diff.
- You've read the relevant code, are genuinely stuck, and want a different model's angle.
- The user asked for it. Then just do it, no lecture.

Budget: **50 calls per day, enforced by the script.** It refuses past that; there is no CLI override. Treat each call as a real cost, not a free lookup. If you're blocked by the cap, answer from the local codebase and say so — do not go editing the `.env` to raise the limit unless the user tells you to.

**Code leaves the machine.** It goes to DeepSeek's servers (China-based). If the repo looks sensitive and the user hasn't already made that call, ask before sending.

The script guards this, but the guard is a net, not a wall — it matches known patterns and will miss a secret that doesn't look like one. You are still responsible for what you put in the glob:

- `.env`, `*.pem`, `*.key`, `id_rsa`, `*credentials*.json` etc. are dropped when they come in via a glob. Naming the exact path overrides that — so don't, unless the user asked for it.
- Any file whose *content* matches a credential pattern (`-----BEGIN`, `sk-ant-`, `ghp_`, `AKIA`, …) hard-blocks the run. Exclude it with `-x`. Only reach for `--allow-secrets` on a genuine false positive, and say so to the user.
- A block is worth mentioning: a live credential sitting in tracked source is a finding in its own right, independent of the question you were asking.

## Script

`scripts/ask_deepseek.py` — stdlib only, no install needed.

```bash
python3 ~/.claude/skills/ask-deepseek/scripts/ask_deepseek.py "QUESTION" -f 'src/**/*.ts'
```

| Flag | Purpose |
|---|---|
| `-f, --files` | file, directory or glob — repeatable; `path:12-40` sends only those lines |
| `-x, --exclude` | exclude glob — repeatable |
| `-d, --diff [REF]` | include `git diff [REF]` |
| `-m, --model` | `deepseek-chat` (default, fast) or `deepseek-reasoner` (slow, deep) |
| `-b, --budget` | max context tokens to pack, default 50000 |
| `--dry-run` | list what would be sent + token estimate, no API call |
| `--allow-secrets` | override the content-based secret block (see above) |

Junk is filtered automatically (`node_modules`, `dist`, `.git`, lockfiles, binaries).

The answer goes to **stdout**; progress, reasoning and token counts go to **stderr**.

## Send the minimum, not the maximum

The instinct is to dump the repo and let DeepSeek sort it out. Resist it. **Send the
smallest slice that can still answer the question**, for three reasons — and the third
is the one people underestimate:

1. Every token costs money and burns budget.
2. Every line you send leaves the user's machine for good.
3. **Noise degrades the answer.** A model given 40 files finds vague problems in all
   of them. Given the 3 that matter, it finds the actual bug. Less context is not a
   compromise here — it's usually a *better* answer.

But minimum means **minimum sufficient**, not minimum possible. Starve it of context
and it hallucinates a plausible answer about code it never saw, or comes back with
"insufficient information" — and that wasted a call from a budget of 50. The target is
the tightest slice a competent engineer would need to answer, and nothing beyond it.

How to actually do it:

- **Locate first, then send.** Grep/glob locally to find *which* code is relevant.
  That's free. Then send only that. Never outsource the search itself.
- **Send functions, not files.** `-f 'src/auth.ts:120-180'` sends exactly those lines.
  Use it when you know the region.
- **`--dry-run` before any real call.** It lists every file with its token count and
  share of the total, biggest first. If one file is 60% of the context and only
  incidental to the question, drop it.
- **Cut the obvious ballast** with `-x`: tests, fixtures, generated code, vendored
  deps — unless they *are* the question.
- **Compensate in prose.** Sending less code means you must say more. Describe what
  you left out and why ("the caller in api.ts just forwards the payload unchanged").
  A tight slice plus a good briefing beats a huge dump.

## Workflow

0. **Check it's warranted.** Re-read "When NOT to use this". If you can answer by
   reading the files, do that instead — it's faster and you'll be more accurate.
1. **Pick the context.** Narrow globs beat `-f .`. Send the minimum sufficient slice
   (see above), then `--dry-run` to confirm what actually goes out.
2. **`--dry-run` first** when you're unsure of the size. If files get dropped, raise `--budget` or narrow the glob rather than sending a truncated pile.
3. **Write a self-contained question.** DeepSeek sees *only* what you send — no chat history, no earlier findings. State the symptom, what you already ruled out, and what a useful answer looks like.
4. **Run it.** Use `-m deepseek-reasoner` for genuinely hard reasoning (subtle bugs, race conditions, architecture); `deepseek-chat` for surveys, "find all usages", mechanical review.
5. **Verify before acting.** DeepSeek only saw a slice and can't run anything. Treat its answer as a lead, not a fact — check claims against the real files before you edit.
6. **Report to the user** what DeepSeek said *and* what you verified. Attribute it: "DeepSeek meint X, ich hab's geprüft — stimmt/stimmt nicht."

## Question quality

The whole value hinges on this. Weak vs. strong:

```
❌ "Was ist hier falsch?"
✅ "Der Checkout schlägt bei ~1% der Requests mit 'order already
   processed' fehl, obwohl der Nutzer nur einmal klickt. Retry-Logik
   in payment.ts und Idempotenz in orders.ts hab ich geprüft, sehen
   korrekt aus. Wo kann derselbe Order zweimal durchlaufen?
   Nenn mir Datei + Funktion."
```

Ask for the shape of the answer you want ("nenn Datei und Zeile", "liste alle Fundstellen", "nur die Top-3 Probleme").

## Recipes

```bash
S=~/.claude/skills/ask-deepseek/scripts/ask_deepseek.py

# Review the current diff
python3 $S "Review this diff for bugs. Only real defects, no style." -d

# Diff against main
python3 $S "Breaking changes for API consumers?" -d main

# Whole-repo survey
python3 $S "Where is user input written to the DB without validation? File+line." \
  -f 'src/**/*.ts' -x '*.test.ts'

# Hard bug, deep model
python3 $S "$(cat bug-report.txt)" -f src/ -m deepseek-reasoner

# Long question via stdin
echo "Explain the auth flow end to end" | python3 $S -f src/auth/

# Minimal context: two known functions, nothing else
python3 $S "Can these two run concurrently and double-charge? File+line." \
  -f 'src/payment.ts:120-180' -f 'src/webhook.ts:40-95'

# Check what a broad glob would actually cost before paying for it
python3 $S "..." -f 'src/**/*.ts' --dry-run
```

## Setup

The key lives in a `.env` file (mode 600, git-ignored):

```
DEEPSEEK_API_KEY=sk-...
```

Lookup order: `$DEEPSEEK_API_KEY` → nearest `.env` walking up from the cwd to `$HOME`
→ `~/.claude/.env` → `~/.claude/deepseek_key`. So a project-local `.env` wins, and a
global one in `~/.claude/.env` covers every other project.
Get a key at https://platform.deepseek.com/api_keys.

When you create a `.env`, `chmod 600` it and confirm `git check-ignore` covers it
**before** the key goes in.

The script names the fix on a placeholder key, `401` (bad key), `402` (out of credit)
and `429` (rate limited). **Never echo the key or paste it into chat** — it would land
in the transcript. Point the user at the file instead.
