"use client";

import { useRouter } from "next/navigation";
import Link from "next/link";
import { useState } from "react";
import { useAuth } from "@/lib/auth-context";

export default function RegisterPage() {
  const { register } = useAuth();
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    try {
      await register(name, email, password);
      router.push("/listings");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Registration failed");
    }
  }

  return (
    <div className="max-w-sm mx-auto mt-10">
      <h1 className="text-2xl font-bold mb-4">Create account</h1>
      <form onSubmit={submit}>
        <input type="text" placeholder="Full name" value={name}
               onChange={(e) => setName(e.target.value)} required />
        <input type="email" placeholder="you@example.com" value={email}
               onChange={(e) => setEmail(e.target.value)} required />
        <input type="password" placeholder="password" value={password}
               onChange={(e) => setPassword(e.target.value)} required />
        {error && <p className="text-primary text-sm my-2">{error}</p>}
        <button className="btn w-full mt-2">Sign up</button>
      </form>
      <p className="text-sm text-gray-500 mt-3 text-center">
        Have an account? <Link href="/login" className="text-primary">Login</Link>
      </p>
    </div>
  );
}
