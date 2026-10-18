"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";

type ColdRoom = {
  id: number;
  name: string;
  location: string;
  commodity: string;
  target_min_c: number;
  target_max_c: number;
  active: boolean;
};

const API_URL = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000").replace(/\/$/, "");

export default function ColdRooms() {
  const [rooms, setRooms] = useState<ColdRoom[]>([]);
  const [name, setName] = useState("");
  const [location, setLocation] = useState("");
  const [commodity, setCommodity] = useState("");
  const [minimum, setMinimum] = useState("2");
  const [maximum, setMaximum] = useState("8");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);

  const loadRooms = useCallback(async () => {
    const response = await fetch(`${API_URL}/api/v1/cold-rooms`);
    if (!response.ok) throw new Error(`API returned HTTP ${response.status}`);
    setRooms((await response.json()) as ColdRoom[]);
  }, []);

  useEffect(() => {
    loadRooms()
      .catch((cause: unknown) => setError(cause instanceof Error ? cause.message : "Could not load cold rooms."))
      .finally(() => setLoading(false));
  }, [loadRooms]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setNotice(null);
    setSaving(true);
    try {
      const response = await fetch(`${API_URL}/api/v1/cold-rooms`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name,
          location,
          commodity,
          target_min_c: Number(minimum),
          target_max_c: Number(maximum),
        }),
      });
      if (!response.ok) {
        const body = (await response.json().catch(() => ({}))) as { detail?: string };
        throw new Error(body.detail || `API returned HTTP ${response.status}`);
      }
      setName("");
      setLocation("");
      setCommodity("");
      setNotice("Cold room registered.");
      await loadRooms();
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Could not register this cold room.");
    } finally {
      setSaving(false);
    }
  }

  const inputClass = "mt-1 w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 outline-none focus:border-emerald-600 focus:ring-2 focus:ring-emerald-600/15";

  return (
    <section className="mt-8 grid gap-6 lg:grid-cols-[1fr_1.2fr]">
      <div className="rounded-2xl border border-slate-200 bg-white p-6">
        <h2 className="text-lg font-semibold">Register a cold room</h2>
        <p className="mt-2 text-sm leading-6 text-slate-500">Add a storage site to the prototype database. Temperature bounds are metadata and must be reviewed for the stored commodity.</p>
        <form onSubmit={handleSubmit} className="mt-5 space-y-4">
          <div>
            <label htmlFor="room-name" className="text-sm font-medium">Storage name</label>
            <input id="room-name" required minLength={2} maxLength={120} value={name} onChange={(e) => setName(e.target.value)} className={inputClass} placeholder="e.g. Ado Produce Store" />
          </div>
          <div>
            <label htmlFor="room-location" className="text-sm font-medium">Location</label>
            <input id="room-location" required minLength={2} maxLength={200} value={location} onChange={(e) => setLocation(e.target.value)} className={inputClass} placeholder="Town, state" />
          </div>
          <div>
            <label htmlFor="room-commodity" className="text-sm font-medium">Commodity</label>
            <input id="room-commodity" required minLength={2} maxLength={100} value={commodity} onChange={(e) => setCommodity(e.target.value)} className={inputClass} placeholder="e.g. Tomatoes" />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label htmlFor="room-min" className="text-sm font-medium">Min temperature (°C)</label>
              <input id="room-min" type="number" step="0.1" required value={minimum} onChange={(e) => setMinimum(e.target.value)} className={inputClass} />
            </div>
            <div>
              <label htmlFor="room-max" className="text-sm font-medium">Max temperature (°C)</label>
              <input id="room-max" type="number" step="0.1" required value={maximum} onChange={(e) => setMaximum(e.target.value)} className={inputClass} />
            </div>
          </div>
          <button disabled={saving} className="w-full rounded-lg bg-emerald-800 px-4 py-3 text-sm font-semibold text-white transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:opacity-60">
            {saving ? "Saving…" : "Register cold room"}
          </button>
        </form>
        {notice && <p role="status" className="mt-3 text-sm text-emerald-700">{notice}</p>}
        {error && <p role="alert" className="mt-3 text-sm text-rose-700">{error}</p>}
      </div>
      <div className="rounded-2xl border border-slate-200 bg-white p-6">
        <div className="flex items-center justify-between gap-3">
          <h2 className="text-lg font-semibold">Registered cold rooms</h2>
          <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">{rooms.length} total</span>
        </div>
        {loading ? (
          <p className="mt-5 text-sm text-slate-500">Loading registered rooms…</p>
        ) : rooms.length === 0 ? (
          <p className="mt-5 rounded-xl bg-slate-50 p-5 text-sm leading-6 text-slate-500">No cold rooms registered yet. Add your first site using the form.</p>
        ) : (
          <div className="mt-4 space-y-3">
            {rooms.map((room) => (
              <article key={room.id} className="rounded-xl border border-slate-200 p-4">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <h3 className="font-semibold">{room.name}</h3>
                    <p className="mt-1 text-sm text-slate-500">{room.location}</p>
                  </div>
                  <span className={`rounded-full px-2.5 py-1 text-xs font-semibold ${room.active ? "bg-emerald-100 text-emerald-800" : "bg-slate-100 text-slate-600"}`}>{room.active ? "Active" : "Inactive"}</span>
                </div>
                <div className="mt-3 flex flex-wrap gap-2 text-xs text-slate-600">
                  <span className="rounded-md bg-slate-100 px-2 py-1">{room.commodity}</span>
                  <span className="rounded-md bg-slate-100 px-2 py-1">{room.target_min_c}–{room.target_max_c}°C target metadata</span>
                  <span className="rounded-md bg-slate-100 px-2 py-1">ID #{room.id}</span>
                </div>
              </article>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}
