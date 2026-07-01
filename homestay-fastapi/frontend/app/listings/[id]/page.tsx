"use client";

import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import type { Place } from "@/lib/types";

export default function PlaceDetailPage() {
  const params = useParams<{ id: string }>();
  const router = useRouter();
  const { user } = useAuth();
  const id = Number(params.id);

  const [place, setPlace] = useState<Place | null>(null);
  const [checkIn, setCheckIn] = useState("");
  const [checkOut, setCheckOut] = useState("");
  const [guests, setGuests] = useState("1");
  const [status, setStatus] = useState("");

  useEffect(() => {
    if (!Number.isNaN(id)) void api.getPlace(id).then(setPlace);
  }, [id]);

  // Booking -> payment flow. The booking is created, then a payment intent,
  // then confirmed (stub mode succeeds instantly).
  async function bookAndPay(e: React.FormEvent) {
    e.preventDefault();
    if (!user) { router.push("/login"); return; }
    setStatus("Creating booking...");
    try {
      const booking = await api.createBooking(
        id, new Date(checkIn).toISOString(), new Date(checkOut).toISOString(), Number(guests),
      );
      setStatus("Processing payment...");
      const intent = await api.createIntent(booking.id);
      await api.confirmPayment(intent.payment_id);
      setStatus("Booked and paid! Redirecting...");
      router.push("/bookings");
    } catch (err) {
      setStatus(err instanceof Error ? err.message : "Something went wrong");
    }
  }

  if (!place) return <p className="text-gray-500">Loading...</p>;

  return (
    <div className="grid md:grid-cols-2 gap-8">
      <div>
        <div className="aspect-video bg-gray-200 rounded-2xl mb-4 overflow-hidden">
          {place.photo && <img src={place.photo} alt={place.title} className="w-full h-full object-cover" />}
        </div>
        <h1 className="text-3xl font-bold">{place.title}</h1>
        <p className="text-gray-500">{place.address}</p>
        <p className="mt-4">{place.description || "A lovely place to stay."}</p>
        <p className="mt-2 text-sm text-gray-500">Up to {place.max_guests} guests</p>
      </div>

      <form onSubmit={bookAndPay} className="card h-fit">
        <p className="text-xl mb-4"><span className="font-bold">${place.price}</span> / night</p>
        <label className="text-sm text-gray-600">Check in</label>
        <input type="date" value={checkIn} onChange={(e) => setCheckIn(e.target.value)} required />
        <label className="text-sm text-gray-600">Check out</label>
        <input type="date" value={checkOut} onChange={(e) => setCheckOut(e.target.value)} required />
        <label className="text-sm text-gray-600">Guests</label>
        <input type="number" min={1} value={guests} onChange={(e) => setGuests(e.target.value)} />
        <button className="btn w-full mt-4">Book &amp; pay</button>
        {status && <p className="text-sm mt-3 text-gray-600">{status}</p>}
        <p className="text-xs text-amber-700 bg-amber-50 rounded-lg p-2 mt-3">
          Demo payment mode: no real card is charged.
        </p>
      </form>
    </div>
  );
}
