export default function AIInsights({ insights }) {
  return (
    <div className="mt-6">
      <h3 className="text-lg font-semibold mb-2">AI Insights</h3>
      <pre className="bg-gray-100 p-3 rounded text-sm overflow-auto">
        {JSON.stringify(insights, null, 2)}
      </pre>
    </div>
  );
}
