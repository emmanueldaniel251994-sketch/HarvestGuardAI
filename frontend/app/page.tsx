const metrics = [
  { label: "Storage status", value: "Monitoring", detail: "Simulated telemetry" },
  { label: "Temperature", value: "4.2°C", detail: "Illustrative reading" },
  { label: "Energy reserve", value: "78%", detail: "Illustrative battery level" },
  { label: "Spoilage risk", value: "Low", detail: "Demo estimate only" },
];

export default function Home() {
  return (
    <main className="min-h-screen bg-[#f4f7f2] text-slate-900">
      <header className="border-b border-emerald-950/10 bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.25em] text-emerald-700">HarvestGuard AI</p>
            <p className="mt-1 text-sm text-slate-500">Predict. Protect. Preserve.</p>
          </div>
          <span className="rounded-full bg-amber-100 px-3 py-1 text-xs font-semibold text-amber-800">Demo data</span>
        </div>
      </header>
      <section className="mx-auto max-w-7xl px-6 py-12">
        <div className="max-w-3xl">
          <p className="text-sm font-semibold text-emerald-700">COLD STORAGE INTELLIGENCE</p>
          <h1 className="mt-3 text-4xl font-semibold tracking-tight sm:text-6xl">Protect every harvest, one signal at a time.</h1>
          <p className="mt-5 max-w-2xl text-lg leading-8 text-slate-600">
            A monitoring and early-warning concept for solar-powered agricultural cold storage.
            This first dashboard uses illustrative values while the simulator and risk engine are built.
          </p>
        </div>
        <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {metrics.map((metric) => (
            <article key={metric.label} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">{metric.label}</p>
              <p className="mt-4 text-3xl font-semibold tracking-tight">{metric.value}</p>
              <p className="mt-2 text-xs text-slate-500">{metric.detail}</p>
            </article>
          ))}
        </div>
        <div className="mt-8 grid gap-6 lg:grid-cols-[1.5fr_1fr]">
          <section className="rounded-2xl border border-slate-200 bg-white p-6">
            <h2 className="text-lg font-semibold">System overview</h2>
            <div className="mt-5 space-y-4">
              {[
                ["Temperature stability", "Tracking simulated readings"],
                ["Solar and battery supply", "Energy analytics coming next"],
                ["Food preservation risk", "Risk scoring engine planned"],
              ].map(([title, detail]) => (
                <div key={title} className="flex items-start justify-between gap-4 border-b border-slate-100 pb-4 last:border-0 last:pb-0">
                  <div><p className="font-medium">{title}</p><p className="mt-1 text-sm text-slate-500">{detail}</p></div>
                  <span className="mt-1 h-2.5 w-2.5 shrink-0 rounded-full bg-amber-400" aria-label="Demo status" />
                </div>
              ))}
            </div>
          </section>
          <aside className="rounded-2xl bg-emerald-950 p-6 text-white">
            <p className="text-sm font-semibold text-emerald-300">BUILD STATUS</p>
            <h2 className="mt-3 text-2xl font-semibold">Foundation phase</h2>
            <p className="mt-3 text-sm leading-6 text-emerald-100/80">Next: connect the API, implement reproducible telemetry simulation, and calculate explainable risk indicators.</p>
            <p className="mt-6 rounded-xl border border-white/15 bg-white/5 p-4 text-xs leading-5 text-emerald-100/80">
              Safety note: this demo is advisory only. It does not control refrigeration, batteries, inverters, or electrical equipment.
            </p>
          </aside>
        </div>
      </section>
      <footer className="mx-auto max-w-7xl px-6 pb-8 text-xs text-slate-500">
        HarvestGuard AI · Early prototype · Simulated readings, not live sensor data
      </footer>
    </main>
  );
}
