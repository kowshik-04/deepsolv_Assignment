export default function PostsList({ posts }) {
  return (
    <div className="mt-6">
      <h3 className="text-lg font-semibold mb-2">Recent Posts</h3>
      <ul className="space-y-2">
        {posts.map((post) => (
          <li
            key={post.post_id}
            className="border rounded p-3 bg-gray-50"
          >
            <p>{post.content}</p>
            <p className="text-sm text-gray-500">
              Likes: {post.likes} • Comments: {post.comments_count}
            </p>
          </li>
        ))}
      </ul>
    </div>
  );
}
