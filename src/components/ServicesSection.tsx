import { GitBranch, Layers, Lightbulb } from "lucide-react";
import servicesImage from "@/assets/services-illustration.jpg";

const services = [
  {
    icon: GitBranch,
    title: "Multi-Agent Orchestration",
    description: "Coordinate multiple AI agents to work together seamlessly on complex tasks."
  },
  {
    icon: Layers,
    title: "API Integrations",
    description: "Connect with hundreds of popular services and APIs for complete automation."
  },
  {
    icon: Lightbulb,
    title: "Smart Recommendations",
    description: "AI-powered insights and suggestions to optimize your automation workflows."
  }
];

export const ServicesSection = () => {
  return (
    <section id="services" className="py-20 px-6">
      <div className="container mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl lg:text-5xl font-bold mb-6">
            Our <span className="gradient-text">Services</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Powerful AI automation tools designed to streamline your workflow and boost productivity
          </p>
        </div>
        
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-glow opacity-30 blur-2xl"></div>
            <img 
              src={servicesImage} 
              alt="Services Illustration" 
              className="relative z-10 w-full h-auto rounded-2xl"
            />
          </div>
          
          <div className="space-y-8">
            {services.map((service, index) => (
              <div key={index} className="glass-card p-6 group hover:shadow-glow-purple transition-all duration-300">
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0">
                    <div className="w-12 h-12 bg-gradient-to-r from-primary to-accent rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform">
                      <service.icon className="w-6 h-6 text-background" />
                    </div>
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-2">{service.title}</h3>
                    <p className="text-muted-foreground">{service.description}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};