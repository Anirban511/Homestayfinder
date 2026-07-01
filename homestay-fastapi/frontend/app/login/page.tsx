"use client";

import { useRouter } from "next/navigation";
import Link from "next/link";
import { useState } from "react";
import { useAuth } from "@/lib/auth-context";

export default function LoginPage() {
  const { login } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    try {
      await login(email, password);
      router.push("/listings");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    }
  }

  return (
    <div className="max-w-sm mx-auto mt-10">
      <h1 className="text-2xl font-bold mb-4">Login</h1>
      <form onSubmit={submit}>
        <input type="email" placeholder="you@example.com" value={email}
               onChange={(e) => setEmail(e.target.value)} required />
        <input type="password" placeholder="password" value={password}
               onChange={(e) => setPassword(e.target.value)} required />
        {error && <p className="text-primary text-sm my-2">{error}</p>}
        <button className="btn w-full mt-2">Login</button>
      </form>
      <p className="text-sm text-gray-500 mt-3 text-center">
        No account? <Link href="/register" className="text-primary">Register</Link>
      </p>
    </div>
  );
}
