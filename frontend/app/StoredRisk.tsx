"use client";

import { useEffect, useState } from "react";

type RiskAssessment = {
  score: number;
  level: "low" | "moderate" | "high" | "critical";
  factors: string[];
  advisory_only: boolean;
};

const API_URL = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000").replace(/\/$/, "");

export default function StoredRisk({ roomId }: { roomId: string }) {
  const [risk, setRisk] = useState<RiskAssessment | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!roomId) {
      setRisk(null);
      setError(null);
      return;
    }
    const controller = new AbortController();
    setLoading(true);
    setError(null);
    fetch(`${API_URL}/api/v1/cold-rooms/${roomId}/risk?limit=24`, { signal: controller.signal })
      .then((response) => {
        if (!response.ok) throw new Error(`Risk API returned HTTP ${response.status}`);
        return response.json() as Promise<RiskAssessment>;
      })
      .then(setRisk)
      .catch((cause: unknown) => {
        if (cause instanceof Error && cause.name === "AbortError") return;
        setError(cause instanceof Error ? cause.message : "Could not calculate stored risk.");
        setRisk(null);
      })
      .finally(() => setLoading(false));
    return () => controller.abort();
  }, [roomId]);

  const levelClass = risk?.level === "critical" || risk?.level === "high"
    ? "bg-rose-100 text-rose-800"
    : risk?.level === "moderate"
      ? "bg-amber-100 text-amber-800"
      : "bg-emerald-100 text-emerald-800";

  return (
    <section className="mt-5 rounded-xl border border-slate-200 p-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-sm font-semibold">Risk assessment from stored readings</p>
          <p className="mt-1 text-xs text-slate-500">Rule-based advisory only; not a trained ML prediction or food-safety certification.</p>
        </div>
        {loading ? <span className="text-sm text-slate-500">Calculating…</span> : risk ? (
          <span className={`rounded-full px-3 py-1 text-sm font-bold ${levelClass}`}>{risk.score}/100 · {risk.level}</span>
        ) : <span className="text-sm text-slate-500">{roomId ? "No risk result" : "Select a cold room"}</span>}
      </div>
      {error && <p role="alert" className="mt-3 text-sm text-rose-700">{error}</p>}
      {risk && <ul className="mt-3 space-y-1 text-sm text-slate-600">{risk.factors.map((factor) => <li key={factor}>• {factor}</li>)}</ul>}
    </section>
  );
}
