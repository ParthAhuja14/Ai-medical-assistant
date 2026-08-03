import { Link, useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { Activity, History, LogOut } from "lucide-react";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const isActive = (path) => location.pathname === path;

  return (
    <header className="border-b border-cardline bg-panel/80 backdrop-blur sticky top-0 z-10">
      <div className="max-w-5xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 font-display text-lg text-ink">
          <Activity className="w-5 h-5 text-teal" strokeWidth={2} />
          Symptomatic
        </Link>

        {user && (
          <nav className="flex items-center gap-6 text-sm">
            <Link
              to="/"
              className={`transition-colors ${isActive("/") ? "text-teal font-medium" : "text-muted hover:text-ink"}`}
            >
              Check symptoms
            </Link>
            <Link
              to="/history"
              className={`flex items-center gap-1.5 transition-colors ${isActive("/history") ? "text-teal font-medium" : "text-muted hover:text-ink"}`}
            >
              <History className="w-4 h-4" />
              History
            </Link>
            <span className="text-cardline">|</span>
            <span className="text-muted">{user.full_name}</span>
            <button
              onClick={handleLogout}
              className="flex items-center gap-1.5 text-muted hover:text-alert transition-colors"
            >
              <LogOut className="w-4 h-4" />
              Sign out
            </button>
          </nav>
        )}
      </div>
    </header>
  );
}
