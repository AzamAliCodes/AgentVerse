import { Button } from "@/components/ui/button";
import { ArrowRight, Zap } from "lucide-react";
import heroImage from "@/assets/rm_bg_logo.png";

export const HeroSection = () => {
  return (
    <section className="min-h-screen flex items-center justify-center pt-20 px-6">
      <div className="container mx-auto grid lg:grid-cols-2 gap-12 items-center">
        <div className="space-y-8">
          <div className="space-y-4">
            <div className="inline-flex items-center space-x-2 glass-card px-4 py-2 rounded-full">
              <Zap className="w-4 h-4 text-primary" />
              <span className="text-sm text-muted-foreground">AI-Powered Automation</span>
            </div>
            <h1 className="text-5xl lg:text-7xl font-bold leading-tight">
              Deploy <span className="gradient-text">AI Agents</span> Effortlessly
            </h1>
            <p className="text-xl text-muted-foreground max-w-2xl">
              Book tickets, manage bookings, fetch reviews, and automate daily tasks—just with a prompt. 
              Transform your workflow with intelligent automation.
            </p>
          </div>
          
          <div className="flex flex-col sm:flex-row gap-4">
            <Button variant="hero" size="lg" className="text-lg">
              Get Started Free
              <ArrowRight className="w-5 h-5" />
            </Button>
            <Button variant="glass" size="lg" className="text-lg">
              Watch Demo
            </Button>
          </div>
          
          <div className="grid grid-cols-3 gap-6 pt-8">
            <div className="glass-card p-4 text-center">
              <div className="text-2xl font-bold gradient-text">100+</div>
              <div className="text-sm text-muted-foreground">Automation Tasks</div>
            </div>
            <div className="glass-card p-4 text-center">
              <div className="text-2xl font-bold gradient-text">99%</div>
              <div className="text-sm text-muted-foreground">Success Rate</div>
            </div>
            <div className="glass-card p-4 text-center">
              <div className="text-2xl font-bold gradient-text">24/7</div>
              <div className="text-sm text-muted-foreground">Support</div>
            </div>
          </div>
        </div>
        
        <div className="relative">
          <div className="absolute inset-0 bg-gradient-glow opacity-50 blur-3xl"></div>
          <img 
            src={heroImage} 
            alt="AI Avatar" 
            className="relative z-10 w-full h-auto rounded-2xl animate-float"
          />
        </div>
      </div>
    </section>
  );
};