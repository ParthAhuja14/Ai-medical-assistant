import { AlertTriangle, MapPin, Pill, Stethoscope } from "lucide-react";

export default function PredictionCard({ prediction, rank, onFindSpecialists }) {
  const { disease, confidence, specialist, medicine_categories, summary, emergency } = prediction;

  return (
    <div
      className={`rounded-xl border p-5 shadow-card bg-panel ${
        emergency ? "border-alert/40" : "border-cardline"
      }`}
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-start gap-3">
          <span className="font-mono text-xs text-muted mt-1.5 tabular-nums">
            {String(rank).padStart(2, "0")}
          </span>
          <div>
            <h3 className="font-display text-xl text-ink leading-snug">{disease}</h3>
            <p className="text-sm text-muted mt-1 leading-relaxed max-w-lg">{summary}</p>
          </div>
        </div>

        <div className="text-right shrink-0">
          <div className="font-mono text-2xl text-teal-dark tabular-nums">{confidence}%</div>
          <div className="text-xs text-muted">confidence</div>
        </div>
      </div>

      <div className="mt-3 h-1.5 w-full bg-cardline rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full ${emergency ? "bg-alert" : "bg-teal"}`}
          style={{ width: `${Math.min(confidence, 100)}%` }}
        />
      </div>

      {emergency && (
        <div className="mt-4 flex items-center gap-2 text-alert bg-alert-light rounded-lg px-3 py-2 text-sm font-medium">
          <AlertTriangle className="w-4 h-4 shrink-0" />
          This condition can be serious — seek medical attention promptly.
        </div>
      )}

      <div className="mt-4 grid sm:grid-cols-2 gap-4 pt-4 border-t border-cardline">
        <div className="flex gap-2.5">
          <Stethoscope className="w-4 h-4 text-teal mt-0.5 shrink-0" />
          <div>
            <div className="text-xs text-muted uppercase tracking-wide">Suggested specialist</div>
            <div className="text-sm text-ink mt-0.5">{specialist}</div>
          </div>
        </div>
        <div className="flex gap-2.5">
          <Pill className="w-4 h-4 text-teal mt-0.5 shrink-0" />
          <div>
            <div className="text-xs text-muted uppercase tracking-wide">General care categories</div>
            <div className="text-sm text-ink mt-0.5">{medicine_categories.join(", ")}</div>
          </div>
        </div>
      </div>

      {rank === 1 && onFindSpecialists && (
        <button
          onClick={onFindSpecialists}
          className="mt-4 inline-flex items-center gap-1.5 text-sm font-medium text-teal-dark hover:text-teal transition-colors"
        >
          <MapPin className="w-4 h-4" />
          Find nearby specialists
        </button>
      )}
    </div>
  );
}
