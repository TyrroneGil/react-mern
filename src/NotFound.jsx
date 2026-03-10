// src/pages/NotFound.jsx
import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <div className="text-center">
      <h1 className="text-4xl font-bold">404</h1>
      <p>Page not found</p>
      <Link to="/" className="text-blue-500 underline">
        Go back home
      </Link>
    </div>
  );
}
