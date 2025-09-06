import { Header } from "@/components/Header";
import { HeroSection } from "@/components/HeroSection";
import { FeaturesBar } from "@/components/FeaturesBar";
import { ServicesSection } from "@/components/ServicesSection";
import { StatsBar } from "@/components/StatsBar";
import { TestimonialsSection } from "@/components/TestimonialsSection";
import { Footer } from "@/components/Footer";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main>
        <HeroSection />
        <FeaturesBar />
        <ServicesSection />
        <StatsBar />
        <TestimonialsSection />
      </main>
      <Footer />
    </div>
  );
};

export default Index;
