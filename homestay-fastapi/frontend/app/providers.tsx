"use client";

import Link from "next/link";
import { AuthProvider, useAuth } from "@/lib/auth-context";
import type { ReactNode } from "react";

function Nav() {
  const { user, logout } = useAuth();
  return (
    <nav className="flex items-center justify-between max-w-5xl mx-auto px-6 py-4">
      <Link href="/" className="font-bold text-xl text-primary">HomestayFinder</Link>
      <div className="flex items-center gap-4 text-sm">
        <Link href="/listings">Browse</Link>
        {user && <Link href="/bookings">My trips</Link>}
        {user?.role === "admin" && <Link href="/analytics">Analytics</Link>}
        {user ? (
          <>
            <span className="text-gray-500">{user.name}</span>
            <button onClick={logout} className="btn-ghost">Logout</button>
          </>
        ) : (
          <>
            <Link href="/login">Login</Link>
            <Link href="/register" className="btn">Sign up</Link>
          </>
        )}
      </div>
    </nav>
  );
}

export function Providers({ children }: { children: ReactNode }) {
  return (
    <AuthProvider>
      <Nav />
      <main className="max-w-5xl mx-auto px-6 py-6">{children}</main>
    </AuthProvider>
  );
}
