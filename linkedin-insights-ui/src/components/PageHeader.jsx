export default function PageHeader({ page }) {
  return (
    <div className="border-b pb-4 mb-4">
      <h2 className="text-2xl font-bold">{page.name}</h2>
      <p className="text-gray-700">{page.description}</p>
      <p className="text-sm text-gray-500">
        Industry: {page.industry} • Followers: {page.followers}
      </p>
    </div>
  );
}
