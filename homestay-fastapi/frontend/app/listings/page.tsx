"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import type { Place } from "@/lib/types";

export default function ListingsPage() {
  const { user } = useAuth();
  const [places, setPlaces] = useState<Place[]>([]);
  const [q, setQ] = useState("");
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [showForm, setShowForm] = useState(false);

  async function load() {
    setPlaces(await api.listPlaces());
  }
  useEffect(() => { void load(); }, []);

  async function search(e: React.FormEvent) {
    e.preventDefault();
    setPlaces(await api.searchPlaces({
      q: q || undefined,
      min_price: minPrice ? Number(minPrice) : undefined,
      max_price: maxPrice ? Number(maxPrice) : undefined,
    }));
  }

  return (
    <div>
      {/* FEATURE: SEARCH */}
      <form onSubmit={search} className="flex flex-wrap gap-2 items-end bg-gray-50 p-4 rounded-2xl mb-6">
        <div className="grow min-w-[180px]">
          <label className="text-sm text-gray-600">Keyword</label>
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="city, title..." />
        </div>
        <div className="w-28">
          <label className="text-sm text-gray-600">Min $</label>
          <input type="number" value={minPrice} onChange={(e) => setMinPrice(e.target.value)} />
        </div>
        <div className="w-28">
          <label className="text-sm text-gray-600">Max $</label>
          <input type="number" value={maxPrice} onChange={(e) => setMaxPrice(e.target.value)} />
        </div>
        <button className="btn">Search</button>
      </form>

      {user && (
        <button onClick={() => setShowForm((s) => !s)} className="btn-ghost mb-4">
          {showForm ? "Close" : "+ Add a listing"}
        </button>
      )}
      {user && showForm && <AddListing onCreated={load} />}

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {places.map((p) => (
          <Link key={p.id} href={`/listings/${p.id}`} className="card hover:shadow-md transition">
            <div className="aspect-square bg-gray-200 rounded-xl mb-3 overflow-hidden">
              {p.photo && <img src={p.photo} alt={p.title} className="w-full h-full object-cover" />}
            </div>
            <h3 className="font-semibold">{p.address}</h3>
            <p className="text-sm text-gray-500">{p.title}</p>
            <p className="mt-1"><span className="font-bold">${p.price}</span> / night</p>
          </Link>
        ))}
      </div>
      {places.length === 0 && <p className="text-gray-500">No listings found.</p>}
    </div>
  );
}

function AddListing({ onCreated }: { onCreated: () => void }) {
  const [title, setTitle] = useState("");
  const [address, setAddress] = useState("");
  const [price, setPrice] = useState("");
  const [guests, setGuests] = useState("2");

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    await api.createPlace({
      title, address, price: Number(price), max_guests: Number(guests), description: "",
    });
    setTitle(""); setAddress(""); setPrice("");
    onCreated();
  }

  return (
    <form onSubmit={submit} className="card mb-6 grid sm:grid-cols-2 gap-2">
      <input placeholder="Title" value={title} onChange={(e) => setTitle(e.target.value)} required />
      <input placeholder="Address / city" value={address} onChange={(e) => setAddress(e.target.value)} required />
      <input type="number" placeholder="Price per night" value={price} onChange={(e) => setPrice(e.target.value)} required />
      <input type="number" placeholder="Max guests" value={guests} onChange={(e) => setGuests(e.target.value)} />
      <button className="btn sm:col-span-2">Create listing</button>
    </form>
  );
}
