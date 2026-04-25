import { useState } from "react";
import { API_BASE } from "../config";

export default function RepoSelector({ setRepo }) {
  const [repoInput, setRepoInput] = useState("");
  const [loadingRepo, setLoadingRepo] = useState(false);
  const [error, setError] = useState("");

  const loadRepo = async () => {
    if (!repoInput.trim() || loadingRepo) return;

    try {
      setLoadingRepo(true);
      setError("");

      const response = await fetch(
        `${API_BASE}/docs/load-repo`,
        {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            repoUrl: repoInput.trim()
          })
        }
      );

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || "Failed to load repository");
      }

      setRepo({
        owner: result.owner,
        name: result.repo,
        fullName: result.full_name,
      });

    } catch (err) {
      setError(err.message || "Repository load failed");

    } finally {
      setLoadingRepo(false);
    }
  };

  return (
    <div className="p-4 border-b">
      <h2 className="font-semibold mb-2">Load Public GitHub Repo</h2>

      <p className="mb-3 text-sm text-gray-500">
        Paste `owner/repo` or a full GitHub URL.
      </p>

      <div className="flex gap-2">
        <input
          value={repoInput}
          onChange={(e) => setRepoInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && loadRepo()}
          placeholder="openai/openai-cookbook"
          className="flex-1 border rounded-lg px-3 py-2 text-sm outline-none"
        />

        <button
          onClick={loadRepo}
          disabled={loadingRepo}
          className="bg-blue-600 text-white px-4 rounded-lg hover:bg-blue-500 disabled:opacity-60"
        >
          {loadingRepo ? "Loading..." : "Load"}
        </button>
      </div>

      {error ? (
        <p className="mt-3 text-sm text-red-500">{error}</p>
      ) : null}
    </div>
  );
}
