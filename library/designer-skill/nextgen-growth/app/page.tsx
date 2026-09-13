import { DreamSkyBackground } from "@/components/dream-sky-background";
import { Navbar } from "@/components/navbar";
import { ShapeHero } from "@/components/shape-hero";
import { Services } from "@/components/services";
import { Process } from "@/components/process";
import { Pricing } from "@/components/pricing";
import { CtaSection } from "@/components/cta-section";
import { Footer } from "@/components/footer";

export default function Home() {
  return (
    <div className="relative min-h-screen" style={{ background: "#fefcff" }}>
      <DreamSkyBackground />
      <Navbar />
      <main>
        <ShapeHero />
        <Services />
        <Process />
        <Pricing />
        <CtaSection />
      </main>
      <Footer />
    </div>
  );
}
