import Link from "next/link";

export default function LandingPage() {
  return (
    <div className="text-center py-20">
      <h1 className="text-5xl font-bold mb-4">Find your next homestay</h1>
      <p className="text-gray-500 max-w-xl mx-auto mb-8">
        Search unique stays, book instantly, pay securely and message your host —
        all in one place.
      </p>
      <div className="flex gap-4 justify-center">
        <Link href="/listings" className="btn">Browse stays</Link>
        <Link href="/register" className="btn-ghost">Become a host</Link>
      </div>
    </div>
  );
}
