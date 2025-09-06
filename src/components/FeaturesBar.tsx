import { Bot, Calendar, Star, Link, Plus } from "lucide-react";

const features = [
  { icon: Bot, name: "Task Automation", color: "text-neon-cyan" },
  { icon: Calendar, name: "Travel Booking", color: "text-neon-purple" },
  { icon: Star, name: "AI Reviews", color: "text-neon-pink" },
  { icon: Link, name: "Integrations", color: "text-neon-green" },
  { icon: Plus, name: "More", color: "text-primary" },
];

export const FeaturesBar = () => {
  return (
    <section className="py-16 px-6">
      <div className="container mx-auto">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
          {features.map((feature, index) => (
            <div 
              key={index}
              className="glass-card p-6 text-center group hover:shadow-glow-cyan transition-all duration-300 cursor-pointer"
            >
              <feature.icon className={`w-8 h-8 mx-auto mb-3 ${feature.color} group-hover:scale-110 transition-transform`} />
              <h3 className="font-semibold text-foreground">{feature.name}</h3>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};