"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import type { Booking } from "@/lib/types";

export default function BookingsPage() {
  const { user, ready } = useAuth();
  const [bookings, setBookings] = useState<Booking[]>([]);

  useEffect(() => {
    if (user) void api.myBookings().then(setBookings);
  }, [user]);

  if (ready && !user) return <p className="text-gray-500">Please log in to see your trips.</p>;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">My trips</h1>
      {bookings.length === 0 && <p className="text-gray-500">No bookings yet.</p>}
      <div className="space-y-3">
        {bookings.map((b) => (
          <div key={b.id} className="card flex justify-between items-center">
            <div>
              <p className="font-semibold">{b.place?.title ?? `Listing #${b.place_id}`}</p>
              <p className="text-sm text-gray-500">
                {new Date(b.check_in).toLocaleDateString()} → {new Date(b.check_out).toLocaleDateString()}
                {" · "}{b.guests} guest(s)
              </p>
            </div>
            <div className="text-right">
              <p className="font-bold">${b.price}</p>
              <span className={`text-xs px-2 py-0.5 rounded-full ${b.payment_status === "paid" ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-600"}`}>
                {b.status} · {b.payment_status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
