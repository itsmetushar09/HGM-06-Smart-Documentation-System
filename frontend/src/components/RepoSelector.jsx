import { useEffect, useState } from "react";
import { API_BASE } from "../config";

export default function RepoSelector({ setRepo }) {

  const [repos, setRepos] = useState([]);
  const [loadingRepo, setLoadingRepo] = useState(null);


  useEffect(() => {

    fetch(`${API_BASE}/auth/github/repos`, {
      credentials: "include"
    })
      .then(res => res.json())
      .then(data => {

        console.log("Repos received:", data);

        setRepos(data);

      });

  }, []);



  const loadRepo = async (repo) => {

    if (loadingRepo === repo.name) return;

    setLoadingRepo(repo.name);

    try {

      const response = await fetch(
        `${API_BASE}/docs/load-repo`,
        {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            owner: repo.owner.login,
            repo: repo.name
          })
        }
      );

      const result = await response.json();

      console.log("Repo loaded:", result);

      // store repo in Docs.jsx state
      setRepo(repo.name);

    } catch (err) {

      console.error("Repo load failed:", err);

    } finally {

      setLoadingRepo(null);

    }
  };



  return (

    <div className="p-4 border-b">

      <h2 className="font-semibold mb-2">Select Repo</h2>

      {repos.map(repo => (

        <div
          key={repo.id}
          onClick={() => loadRepo(repo)}
          className="cursor-pointer hover:bg-gray-200 p-2 rounded"
        >
          {repo.name}
        </div>

      ))}

    </div>

  );
}