"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import StoredRisk from "./StoredRisk";

type ColdRoom = {
  id: number;
  name: string;
  location: string;
  commodity: string;
  target_min_c: number;
  target_max_c: number;
  active: boolean;
};

type Reading = {
  id?: number;
  cold_room_id?: number;
  timestamp: string;
  temperature_c: number;
  humidity_pct: number;
  battery_pct: number;
  solar_power_w: number;
  load_power_w: number;
};

type DemoPayload = { readings: Reading[] };

const API_URL = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000").replace(/\/$/, "");

export default function ColdRooms() {
  const [rooms, setRooms] = useState<ColdRoom[]>([]);
  const [selectedRoomId, setSelectedRoomId] = useState("");
  const [history, setHistory] = useState<Reading[]>([]);
  const [riskRefreshKey, setRiskRefreshKey] = useState(0);
  const [name, setName] = useState("");
  const [location, setLocation] = useState("");
  const [commodity, setCommodity] = useState("");
  const [minimum, setMinimum] = useState("2");
  const [maximum, setMaximum] = useState("8");
  const [loading, setLoading] = useState(true);
  const [loadingHistory, setLoadingHistory] = useState(false);
  const [saving, setSaving] = useState(false);
  const [seeding, setSeeding] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);

  const loadRooms = useCallback(async () => {
    const response = await fetch(`${API_URL}/api/v1/cold-rooms`);
    if (!response.ok) throw new Error(`API returned HTTP ${response.status}`);
    const result = (await response.json()) as ColdRoom[];
    setRooms(result);
    setSelectedRoomId((current) => current || (result[0] ? String(result[0].id) : ""));
  }, []);

  const loadHistory = useCallback(async (roomId: string) => {
    if (!roomId) {
      setHistory([]);
      return;
    }
    setLoadingHistory(true);
    try {
      const response = await fetch(`${API_URL}/api/v1/cold-rooms/${roomId}/readings?limit=100`);
      if (!response.ok) throw new Error(`History API returned HTTP ${response.status}`);
      setHistory((await response.json()) as Reading[]);
    } finally {
      setLoadingHistory(false);
    }
  }, []);

  useEffect(() => {
    loadRooms()
      .catch((cause: unknown) => setError(cause instanceof Error ? cause.message : "Could not load cold rooms."))
      .finally(() => setLoading(false));
  }, [loadRooms]);

  useEffect(() => {
    loadHistory(selectedRoomId).catch((cause: unknown) => {
      setError(cause instanceof Error ? cause.message : "Could not load stored readings.");
    });
  }, [selectedRoomId, loadHistory]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setNotice(null);
    if (Number(minimum) >= Number(maximum)) {
      setError("Minimum temperature must be lower than maximum temperature.");
      return;
    }
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
      const created = (await response.json()) as ColdRoom;
      setName("");
      setLocation("");
      setCommodity("");
      await loadRooms();
      setSelectedRoomId(String(created.id));
      setNotice("Cold room registered successfully.");
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Could not register this cold room.");
    } finally {
      setSaving(false);
    }
  }

  async function saveDemoReadings() {
    if (!selectedRoomId) return;
    setError(null);
    setNotice(null);
    setSeeding(true);
    try {
      const response = await fetch(
        API_URL + "/api/v1/cold-rooms/" + selectedRoomId + "/readings/demo?samples=24&seed=42",
        { method: "POST" },
      );
      if (!response.ok) {
        const body = (await response.json().catch(() => ({}))) as { detail?: string };
        throw new Error(body.detail || ("Could not save demo readings (HTTP " + response.status + ")."));
      }
      const saved = (await response.json()) as Reading[];
      await loadHistory(selectedRoomId);
      setRiskRefreshKey((current) => current + 1);
      setNotice("Saved " + saved.length + " simulated readings to this cold room. These are demo data, not sensor measurements.");
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Could not save demo readings.");
      await loadHistory(selectedRoomId).catch(() => undefined);
    } finally {
      setSeeding(false);
    }
  }
  function exportReadingsCsv() {
    if (!history.length) return;
    const columns: (keyof Reading)[] = [
      "timestamp", "temperature_c", "humidity_pct", "battery_pct", "solar_power_w", "load_power_w",
    ];
    const cell = (value: unknown) => {
      const text = String(value ?? "");
      return /[",\r\n]/.test(text) ? '"' + text.replace(/"/g, '""') + '"' : text;
    };
    const csv = [
      columns.join(","),
      ...history.map((reading) => columns.map((column) => cell(reading[column])).join(",")),
    ].join("\r\n");
    const blob = new Blob(["\uFEFF", csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "harvestguard-room-" + selectedRoomId + "-readings.csv";
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(url);
  }

  const selectedRoom = rooms.find((room) => String(room.id) === selectedRoomId);

  return (
    <section className="mt-8 space-y-6">
      <div className="grid gap-6 lg:grid-cols-[1fr_1.2fr]">
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
            <>
              <label htmlFor="selected-room" className="mt-5 block text-sm font-medium">Choose a site to view its stored readings</label>
              <select id="selected-room" value={selectedRoomId} onChange={(e) => setSelectedRoomId(e.target.value)} className={inputClass}>
                {rooms.map((room) => <option key={room.id} value={room.id}>{room.name} — {room.location}</option>)}
              </select>
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
                      <span className="rounded-md bg-slate-100 px-2 py-1">{room.target_min_c}–{room.target_max_c}°C configured range</span>
                      <span className="rounded-md bg-slate-100 px-2 py-1">ID #{room.id}</span>
                    </div>
                  </article>
                ))}
              </div>
            </>
          )}
        </div>
      </div>

      <section className="rounded-2xl border border-slate-200 bg-white p-6">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.2em] text-emerald-700">Persistent telemetry</p>
            <h2 className="mt-2 text-xl font-semibold">{selectedRoom ? selectedRoom.name : "Reading history"}</h2>
            <p className="mt-1 text-sm text-slate-500">Readings saved for the selected cold room in the API database.</p>
          </div>
          <button type="button" disabled={!selectedRoomId || seeding} onClick={saveDemoReadings} className="rounded-lg bg-emerald-800 px-4 py-3 text-sm font-semibold text-white hover:bg-emerald-700 disabled:cursor-not-allowed disabled:opacity-60">
            {seeding ? "Saving demo readings…" : "Save 24 demo readings"}
          </button>
        </div>
        <p className="mt-3 rounded-lg bg-amber-50 p-3 text-xs leading-5 text-amber-900">Demo-only action: this writes synthetic readings into the database. It does not connect to a sensor, and repeated clicks create additional records.</p>
        <StoredRisk roomId={selectedRoomId} refreshKey={riskRefreshKey} />
        {notice && <p role="status" className="mt-3 text-sm text-emerald-700">{notice}</p>}
        {error && <p role="alert" className="mt-3 text-sm text-rose-700">{error}</p>}
        <div className="mt-5 flex items-center justify-between gap-3">
          <div className="flex items-center gap-3"><h3 className="font-semibold">Stored readings</h3><button type="button" disabled={!history.length || loadingHistory} onClick={exportReadingsCsv} className="rounded-lg border border-slate-300 px-3 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50">Export CSV</button></div>
          <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">{history.length} shown</span>
        </div>
        {loadingHistory ? (
          <p className="mt-4 text-sm text-slate-500">Loading reading history…</p>
        ) : history.length === 0 ? (
          <p className="mt-4 rounded-xl bg-slate-50 p-5 text-sm text-slate-500">No stored readings for this site yet. Use the demo button to populate sample data.</p>
        ) : (
          <div className="mt-4 overflow-x-auto">
            <table className="w-full min-w-[640px] text-left text-sm">
              <thead><tr className="border-b border-slate-200 text-xs uppercase tracking-wide text-slate-500"><th className="py-3 pr-4">Timestamp</th><th className="py-3 pr-4">Temp °C</th><th className="py-3 pr-4">Humidity</th><th className="py-3 pr-4">Battery</th><th className="py-3 pr-4">Solar W</th><th className="py-3">Load W</th></tr></thead>
              <tbody>
                {history.slice(0, 20).map((reading, index) => (
                  <tr key={reading.id ?? `${reading.timestamp}-${index}`} className="border-b border-slate-100 last:border-0">
                    <td className="py-3 pr-4 text-slate-500">{new Date(reading.timestamp).toLocaleString()}</td>
                    <td className="py-3 pr-4 font-medium tabular-nums">{reading.temperature_c.toFixed(1)}</td>
                    <td className="py-3 pr-4 tabular-nums">{reading.humidity_pct.toFixed(1)}%</td>
                    <td className="py-3 pr-4 tabular-nums">{reading.battery_pct.toFixed(1)}%</td>
                    <td className="py-3 pr-4 tabular-nums">{reading.solar_power_w.toFixed(0)}</td>
                    <td className="py-3 tabular-nums">{reading.load_power_w.toFixed(0)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            {history.length > 20 && <p className="mt-3 text-xs text-slate-500">Showing 20 of {history.length} readings. The API request retrieves up to 100.</p>}
          </div>
        )}
      </section>
    </section>
  );
}
