import { useEffect, useState } from "react";
import { diagnosisService } from "../services/diagnosisService";
import { AlertTriangle, Calendar } from "lucide-react";

function formatSymptomLabel(raw) {
  return raw.replace(/_/g, " ");
}

export default function History() {
  const [sessions, setSessions] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    diagnosisService
      .history()
      .then(({ data }) => setSessions(data))
      .catch(() => setError("Could not load your history."));
  }, []);

  return (
    <div className="max-w-2xl mx-auto px-6 py-12">
      <h1 className="font-display text-2xl text-ink mb-1">Your history</h1>
      <p className="text-muted mb-8">Past symptom checks and their top predictions.</p>

      {error && <p className="text-sm text-alert">{error}</p>}

      {sessions && sessions.length === 0 && (
        <p className="text-muted text-sm">You haven't checked any symptoms yet.</p>
      )}

      <div className="space-y-3">
        {sessions?.map((s) => {
          const top = s.predictions?.[0];
          return (
            <div
              key={s.id}
              className={`rounded-xl border p-4 bg-panel ${
                s.is_emergency ? "border-alert/30" : "border-cardline"
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 text-xs text-muted">
                  <Calendar className="w-3.5 h-3.5" />
                  {new Date(s.created_at).toLocaleDateString(undefined, {
                    year: "numeric",
                    month: "short",
                    day: "numeric",
                  })}
                </div>
                {s.is_emergency && (
                  <span className="flex items-center gap-1 text-xs font-medium text-alert">
                    <AlertTriangle className="w-3.5 h-3.5" />
                    Flagged urgent
                  </span>
                )}
              </div>

              {top && (
                <p className="font-display text-lg text-ink mt-2">
                  {top.disease}{" "}
                  <span className="font-mono text-sm text-teal-dark">{top.confidence}%</span>
                </p>
              )}

              <p className="text-sm text-muted mt-1">
                {s.reported_symptoms.slice(0, 4).map(formatSymptomLabel).join(", ")}
                {s.reported_symptoms.length > 4 && ` +${s.reported_symptoms.length - 4} more`}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
