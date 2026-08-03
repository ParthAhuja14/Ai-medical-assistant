import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { Activity } from "lucide-react";
import PulseDivider from "../components/PulseDivider";

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await register(fullName, email, password);
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.detail || "Could not create your account.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-6">
      <div className="w-full max-w-sm">
        <div className="flex items-center gap-2 justify-center mb-2">
          <Activity className="w-6 h-6 text-teal" />
          <span className="font-display text-2xl text-ink">Symptomatic</span>
        </div>
        <PulseDivider />
        <h1 className="font-display text-lg text-center text-muted mb-8">Create your account</h1>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-ink mb-1.5">Full name</label>
            <input
              type="text"
              required
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              className="w-full px-4 py-2.5 rounded-lg border border-cardline focus:border-teal transition-colors"
              placeholder="Jane Doe"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-ink mb-1.5">Email</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2.5 rounded-lg border border-cardline focus:border-teal transition-colors"
              placeholder="you@example.com"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-ink mb-1.5">Password</label>
            <input
              type="password"
              required
              minLength={6}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2.5 rounded-lg border border-cardline focus:border-teal transition-colors"
              placeholder="At least 6 characters"
            />
          </div>

          {error && <p className="text-sm text-alert">{error}</p>}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-teal hover:bg-teal-dark text-white font-medium py-2.5 rounded-lg transition-colors disabled:opacity-60"
          >
            {loading ? "Creating account…" : "Create account"}
          </button>
        </form>

        <p className="text-center text-sm text-muted mt-6">
          Already have an account?{" "}
          <Link to="/login" className="text-teal-dark font-medium hover:text-teal">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
