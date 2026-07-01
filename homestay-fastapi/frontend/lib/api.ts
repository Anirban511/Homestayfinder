// Typed API client. A single fetch wrapper attaches the JWT and parses JSON,
// with one typed helper per endpoint group.
import type {
  Analytics, AdminStats, Booking, PaymentIntent, Place, SearchParams, User,
} from "./types";

const BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const TOKEN_KEY = "hsf_token";

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem(TOKEN_KEY);
}
export function setToken(token: string): void {
  window.localStorage.setItem(TOKEN_KEY, token);
}
export function clearToken(): void {
  window.localStorage.removeItem(TOKEN_KEY);
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string> | undefined),
  };
  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${BASE}${path}`, { ...options, headers });
  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    throw new Error((detail as { detail?: string }).detail || `Request failed: ${res.status}`);
  }
  if (res.status === 204) return undefined as T;
  return (await res.json()) as T;
}

function qs(params: Record<string, unknown>): string {
  const entries = Object.entries(params).filter(([, v]) => v !== undefined && v !== "");
  if (entries.length === 0) return "";
  return "?" + entries.map(([k, v]) => `${k}=${encodeURIComponent(String(v))}`).join("&");
}

export const api = {
  // auth
  register: (name: string, email: string, password: string) =>
    request<User>("/api/auth/register", { method: "POST", body: JSON.stringify({ name, email, password }) }),
  login: (email: string, password: string) =>
    request<{ access_token: string }>("/api/auth/login", { method: "POST", body: JSON.stringify({ email, password }) }),
  me: () => request<User>("/api/auth/me"),

  // places
  listPlaces: () => request<Place[]>("/api/places"),
  searchPlaces: (params: SearchParams) =>
    request<Place[]>(`/api/places/search${qs(params as Record<string, unknown>)}`),
  getPlace: (id: number) => request<Place>(`/api/places/${id}`),
  createPlace: (body: Partial<Place>) =>
    request<Place>("/api/places", { method: "POST", body: JSON.stringify(body) }),

  // bookings
  createBooking: (place_id: number, check_in: string, check_out: string, guests: number) =>
    request<Booking>("/api/bookings", { method: "POST", body: JSON.stringify({ place_id, check_in, check_out, guests }) }),
  myBookings: () => request<Booking[]>("/api/bookings"),

  // payments
  createIntent: (booking_id: number) =>
    request<PaymentIntent>("/api/payments/create-intent", { method: "POST", body: JSON.stringify({ booking_id }) }),
  confirmPayment: (payment_id: number) =>
    request<{ ok: boolean }>("/api/payments/confirm", { method: "POST", body: JSON.stringify({ payment_id }) }),

  // admin / analytics
  adminStats: () => request<AdminStats>("/api/admin/stats"),
  analytics: () => request<Analytics>("/api/admin/analytics"),
};
