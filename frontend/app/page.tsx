import DemoTelemetry from "./DemoTelemetry";
import ColdRooms from "./ColdRooms";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#f4f7f2] text-slate-900">
      <header className="border-b border-emerald-950/10 bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.25em] text-emerald-700">HarvestGuard AI</p>
            <p className="mt-1 text-sm text-slate-500">Predict. Protect. Preserve.</p>
          </div>
          <span className="rounded-full bg-amber-100 px-3 py-1 text-xs font-semibold text-amber-800">Prototype · Simulated data</span>
        </div>
      </header>
      <section className="mx-auto max-w-7xl px-6 py-12">
        <div className="max-w-3xl">
          <p className="text-sm font-semibold text-emerald-700">COLD STORAGE INTELLIGENCE</p>
          <h1 className="mt-3 text-4xl font-semibold tracking-tight sm:text-6xl">Protect every harvest, one signal at a time.</h1>
          <p className="mt-5 max-w-2xl text-lg leading-8 text-slate-600">
            A monitoring and early-warning concept for solar-powered agricultural cold storage.
            The dashboard retrieves synthetic telemetry from the HarvestGuard API and explains the prototype risk score.
          </p>
        </div>
        <DemoTelemetry />
        <ColdRooms />
        <section className="mt-8 rounded-2xl border border-slate-200 bg-white p-6">
          <h2 className="text-lg font-semibold">What comes next</h2>
          <div className="mt-4 grid gap-4 sm:grid-cols-3">
            <div><p className="font-medium">Persistent cold-room records</p><p className="mt-1 text-sm text-slate-500">Store locations, commodity profiles, and sensor metadata.</p></div>
            <div><p className="font-medium">Validated risk indicators</p><p className="mt-1 text-sm text-slate-500">Add missing-data checks and commodity-specific thresholds with domain review.</p></div>
            <div><p className="font-medium">Model evaluation</p><p className="mt-1 text-sm text-slate-500">Compare any ML model with a transparent baseline before making predictive claims.</p></div>
          </div>
        </section>
      </section>
      <footer className="mx-auto max-w-7xl px-6 pb-8 text-xs text-slate-500">
        HarvestGuard AI · Early prototype · Simulated readings, not live sensor data
      </footer>
    </main>
  );
}
