"use client";

import { useEffect, useState } from "react";
import {
  Bar, BarChart, CartesianGrid, Cell, Legend, Line, LineChart,
  ResponsiveContainer, Tooltip, XAxis, YAxis,
} from "recharts";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import type { Analytics } from "@/lib/types";

const COLORS = ["#F5385D", "#3B82F6", "#10B981", "#F59E0B"];

export default function AnalyticsPage() {
  const { user, ready } = useAuth();
  const [data, setData] = useState<Analytics | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (user?.role === "admin") {
      api.analytics().then(setData).catch((e) => setError(e.message));
    }
  }, [user]);

  if (ready && (!user || user.role !== "admin")) {
    return <p className="text-gray-500">Admin access required. Promote your account with make_admin.py.</p>;
  }
  if (error) return <p className="text-primary">{error}</p>;
  if (!data) return <p className="text-gray-500">Loading analytics...</p>;

  const { stats, bookings_by_status, revenue_by_day } = data;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Analytics</h1>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <Stat label="Users" value={stats.users} />
        <Stat label="Listings" value={stats.places} />
        <Stat label="Bookings" value={stats.bookings} />
        <Stat label="Revenue" value={`$${stats.revenue}`} />
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        <div className="card">
          <h2 className="font-semibold mb-4">Bookings by status</h2>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={bookings_by_status}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="label" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="value">
                {bookings_by_status.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h2 className="font-semibold mb-4">Revenue by day</h2>
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={revenue_by_day}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="label" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="value" name="Revenue" stroke="#F5385D" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: number | string }) {
  return (
    <div className="card">
      <p className="text-sm text-gray-500">{label}</p>
      <p className="text-2xl font-bold">{value}</p>
    </div>
  );
}
