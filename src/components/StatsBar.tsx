const stats = [
  { value: "10K+", label: "Active Users" },
  { value: "1M+", label: "Automations" },
  { value: "99.9%", label: "Uptime" },
  { value: "24/7", label: "Support" },
];

export const StatsBar = () => {
  return (
    <section className="py-16 px-6">
      <div className="container mx-auto">
        <div className="glass-card p-8">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-3xl lg:text-4xl font-bold gradient-text mb-2">
                  {stat.value}
                </div>
                <div className="text-muted-foreground font-medium">
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};