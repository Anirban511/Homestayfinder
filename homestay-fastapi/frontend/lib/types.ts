// Shared API types, kept in one place so pages and the client agree on shapes.
export interface User {
  id: number;
  name: string;
  email: string;
  role: "user" | "admin";
}

export interface Place {
  id: number;
  owner_id: number;
  title: string;
  address: string;
  description: string;
  price: number;
  max_guests: number;
  photo: string;
  created_at?: string;
}

export interface Booking {
  id: number;
  place_id: number;
  user_id: number;
  check_in: string;
  check_out: string;
  guests: number;
  price: number;
  status: string;
  payment_status: string;
  place?: Place;
}

export interface PaymentIntent {
  payment_id: number;
  client_secret: string;
  mode: string;
  amount: number;
}

export interface AdminStats {
  users: number;
  places: number;
  bookings: number;
  revenue: number;
}

export interface PricePoint {
  label: string;
  value: number;
}

export interface Analytics {
  stats: AdminStats;
  bookings_by_status: PricePoint[];
  revenue_by_day: PricePoint[];
}

export interface SearchParams {
  q?: string;
  min_price?: number;
  max_price?: number;
  guests?: number;
}
