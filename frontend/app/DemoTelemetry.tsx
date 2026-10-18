"use client";

import { useEffect, useState } from "react";

type Reading = {
  timestamp: string;
  temperature_c: number;
  humidity_pct: number;
  battery_pct: number;
  solar_power_w: number;
  load_power_w: number;
};

type Payload = {
  mode: "simulated";
  readings: Reading[];
  risk: {
    score: number;
    level: "low" | "moderate" | "high" | "critical";
    factors: string[];
    advisory_only: boolean;
  };
  notice: string;
};

const API_URL = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000").replace(/\/$/, "");

function Metric({ label, value, detail }: { label: string; value: string; detail: string }) {
  return (
    <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <p className="text-sm text-slate-500">{label}</p>
      <p className="mt-4 text-3xl font-semibold tracking-tight">{value}</p>
      <p className="mt-2 text-xs text-slate-500">{detail}</p>
    </article>
  );
}

export default function DemoTelemetry() {
  const [data, setData] = useState<Payload | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const controller = new AbortController();
    fetch(`${API_URL}/api/v1/demo/telemetry?samples=24&seed=42`, { signal: controller.signal })
      .then((response) => {
        if (!response.ok) throw new Error(`API returned HTTP ${response.status}`);
        return response.json() as Promise<Payload>;
      })
      .then(setData)
      .catch((cause: unknown) => {
        if (cause instanceof Error && cause.name === "AbortError") return;
        setError(cause instanceof Error ? cause.message : "Could not load demo telemetry.");
      })
      .finally(() => setLoading(false));
    return () => controller.abort();
  }, []);

  const latest = data?.readings[data.readings.length - 1];
  const riskClass = data?.risk.level === "critical" || data?.risk.level === "high"
    ? "bg-rose-100 text-rose-800"
    : data?.risk.level === "moderate"
      ? "bg-amber-100 text-amber-800"
      : "bg-emerald-100 text-emerald-800";

  return (
    <>
      {error && (
        <div role="alert" className="mt-8 rounded-xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-800">
          Could not reach the demo API ({error}). Start the backend and check NEXT_PUBLIC_API_URL.
        </div>
      )}
      {loading && <p className="mt-8 text-sm text-slate-500">Loading simulated telemetry…</p>}
      {data && latest && (
        <>
          <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <Metric label="Latest temperature" value={`${latest.temperature_c.toFixed(1)}°C`} detail="Simulated reading" />
            <Metric label="Battery reserve" value={`${latest.battery_pct.toFixed(0)}%`} detail="Simulated state of charge" />
            <Metric label="Solar generation" value={`${latest.solar_power_w.toFixed(0)} W`} detail="Illustrative power output" />
            <Metric label="Advisory risk" value={`${data.risk.score}/100`} detail={data.risk.level.toUpperCase()} />
          </div>
          <div className="mt-8 grid gap-6 lg:grid-cols-[1.5fr_1fr]">
            <section className="rounded-2xl border border-slate-200 bg-white p-6">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <h2 className="text-lg font-semibold">Latest telemetry</h2>
                <span className="rounded-full bg-amber-100 px-3 py-1 text-xs font-semibold text-amber-800">SIMULATED DATA</span>
              </div>
              <div className="mt-5 divide-y divide-slate-100">
                {[
                  ["Temperature", `${latest.temperature_c.toFixed(1)} °C`],
                  ["Relative humidity", `${latest.humidity_pct.toFixed(1)}%`],
                  ["Battery reserve", `${latest.battery_pct.toFixed(1)}%`],
                  ["Solar power", `${latest.solar_power_w.toFixed(1)} W`],
                  ["Electrical load", `${latest.load_power_w.toFixed(1)} W`],
                ].map(([label, value]) => (
                  <div key={label} className="flex items-center justify-between gap-4 py-3 text-sm">
                    <span className="text-slate-600">{label}</span><span className="font-semibold tabular-nums">{value}</span>
                  </div>
                ))}
              </div>
              <p className="mt-4 text-xs text-slate-400">Sample timestamp: {new Date(latest.timestamp).toLocaleString()}</p>
            </section>
            <aside className="rounded-2xl bg-emerald-950 p-6 text-white">
              <p className="text-sm font-semibold text-emerald-300">RISK ENGINE</p>
              <div className="mt-3 flex items-center justify-between gap-3">
                <h2 className="text-2xl font-semibold">Advisory assessment</h2>
                <span className={`rounded-full px-3 py-1 text-xs font-bold ${riskClass}`}>{data.risk.level}</span>
              </div>
              <p className="mt-3 text-sm leading-6 text-emerald-100/80">Prototype rule-based score: {data.risk.score} out of 100.</p>
              <ul className="mt-5 space-y-3 text-sm text-emerald-50">
                {data.risk.factors.map((factor) => <li key={factor} className="flex gap-2"><span aria-hidden="true">•</span><span>{factor}</span></li>)}
              </ul>
              <p className="mt-6 rounded-xl border border-white/15 bg-white/5 p-4 text-xs leading-5 text-emerald-100/80">{data.notice} The prototype thresholds are not validated food-safety advice.</p>
            </aside>
          </div>
        </>
      )}
    </>
  );
}
