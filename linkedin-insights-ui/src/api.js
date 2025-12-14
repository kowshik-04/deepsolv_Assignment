const API_BASE = "http://127.0.0.1:8000/api";

export async function fetchPage(pageId) {
  const res = await fetch(`${API_BASE}/pages/${pageId}`);
  if (!res.ok) throw new Error("Failed to fetch page");
  return res.json();
}

export async function fetchPosts(pageId) {
  const res = await fetch(`${API_BASE}/pages/${pageId}/posts?limit=15`);
  if (!res.ok) throw new Error("Failed to fetch posts");
  return res.json();
}

export async function fetchEmployees(pageId) {
  const res = await fetch(`${API_BASE}/pages/${pageId}/employees`);
  if (!res.ok) throw new Error("Failed to fetch employees");
  return res.json();
}

export async function fetchAIInsights(pageId) {
  const res = await fetch(`${API_BASE}/pages/${pageId}/ai-insights`);
  if (!res.ok) throw new Error("Failed to fetch AI insights");
  return res.json();
}
