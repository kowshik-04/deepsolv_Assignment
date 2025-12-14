import { useState } from "react";
import {
  fetchPage,
  fetchPosts,
  fetchEmployees,
  fetchAIInsights
} from "./api";

import PageHeader from "./components/PageHeader";
import PostsList from "./components/PostsList";
import EmployeesList from "./components/EmployeesList";
import AIInsights from "./components/AIInsights";

function App() {
  const [pageId, setPageId] = useState("");
  const [page, setPage] = useState(null);
  const [posts, setPosts] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [ai, setAI] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadData = async () => {
    setLoading(true);
    setError("");

    try {
      const pageData = await fetchPage(pageId);
      setPage(pageData);

      const [postsData, empData, aiData] = await Promise.all([
        fetchPosts(pageId),
        fetchEmployees(pageId),
        fetchAIInsights(pageId)
      ]);

      setPosts(postsData);
      setEmployees(empData);
      setAI(aiData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-5xl mx-auto bg-white p-6 rounded shadow">
        <h1 className="text-3xl font-bold mb-4">
          LinkedIn Insights Dashboard
        </h1>

        <div className="flex gap-2 mb-4">
          <input
            className="border p-2 flex-1 rounded"
            placeholder="Enter LinkedIn Page ID (e.g. deepsolv)"
            value={pageId}
            onChange={(e) => setPageId(e.target.value)}
          />
          <button
            onClick={loadData}
            className="bg-blue-600 text-white px-4 rounded"
          >
            Load
          </button>
        </div>

        {loading && <p className="text-blue-600">Loading...</p>}
        {error && <p className="text-red-600">{error}</p>}

        {page && <PageHeader page={page} />}
        {ai && <AIInsights insights={ai} />}
        {posts.length > 0 && <PostsList posts={posts} />}
        {employees.length > 0 && (
          <EmployeesList employees={employees} />
        )}
      </div>
    </div>
  );
}

export default App;
