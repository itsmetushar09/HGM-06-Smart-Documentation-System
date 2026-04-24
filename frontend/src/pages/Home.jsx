export default function Home() {
  return (
    <div className="h-screen flex flex-col items-center justify-center gap-4">
      <h1 className="text-3xl">🚀 Smart Docs Home Page</h1>

      <button
        onClick={() => window.location.href = "/docs"}
        className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-500"
      >
        Go to Docs
      </button>
    </div>
  );
}
