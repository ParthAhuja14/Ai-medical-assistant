import { useLocation, useNavigate, Link } from "react-router-dom";
import { useState } from "react";
import { AlertTriangle, ArrowLeft, MapPin } from "lucide-react";
import PredictionCard from "../components/PredictionCard";
import DisclaimerBanner from "../components/DisclaimerBanner";
import { diagnosisService } from "../services/diagnosisService";

export default function Results() {
  const location = useLocation();
  const navigate = useNavigate();
  const result = location.state?.result;

  const [specialists, setSpecialists] = useState(null);
  const [specialistsLoading, setSpecialistsLoading] = useState(false);
  const [specialistsNote, setSpecialistsNote] = useState("");

  if (!result) {
    return (
      <div className="max-w-2xl mx-auto px-6 py-16 text-center">
        <p className="text-muted">No results to show yet.</p>
        <Link to="/" className="text-teal-dark font-medium hover:text-teal">
          Check your symptoms
        </Link>
      </div>
    );
  }

  const handleFindSpecialists = async () => {
    setSpecialistsLoading(true);
    setSpecialistsNote("");
    try {
      const { data } = await diagnosisService.nearbySpecialists(result.id);
      setSpecialists(data.results);
      setSpecialistsNote(data.note || "");
    } catch (err) {
      setSpecialistsNote(
        err.response?.data?.detail || "Could not find nearby specialists right now."
      );
    } finally {
      setSpecialistsLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto px-6 py-12">
      <button
        onClick={() => navigate("/")}
        className="flex items-center gap-1.5 text-sm text-muted hover:text-ink transition-colors mb-6"
      >
        <ArrowLeft className="w-4 h-4" />
        Check different symptoms
      </button>

      {result.is_emergency && (
        <div className="mb-6 flex items-start gap-3 bg-alert-light border border-alert/30 rounded-xl px-5 py-4">
          <AlertTriangle className="w-5 h-5 text-alert shrink-0 mt-0.5" />
          <div>
            <p className="font-semibold text-alert">This may need urgent attention</p>
            {result.red_flags.map((flag, i) => (
              <p key={i} className="text-sm text-ink/80 mt-1">{flag}</p>
            ))}
          </div>
        </div>
      )}

      <h1 className="font-display text-2xl text-ink mb-1">Your results</h1>
      <p className="text-muted leading-relaxed mb-6">{result.llm_explanation}</p>

      <div className="space-y-4">
        {result.predictions.map((p, i) => (
          <PredictionCard
            key={p.disease}
            prediction={p}
            rank={i + 1}
            onFindSpecialists={i === 0 ? handleFindSpecialists : null}
          />
        ))}
      </div>

      {(specialistsLoading || specialists || specialistsNote) && (
        <div className="mt-6 rounded-xl border border-cardline bg-panel p-5">
          <h2 className="font-display text-lg text-ink flex items-center gap-2">
            <MapPin className="w-4 h-4 text-teal" />
            Nearby specialists
          </h2>
          {specialistsLoading && <p className="text-sm text-muted mt-2">Searching nearby…</p>}
          {specialistsNote && <p className="text-sm text-muted mt-2">{specialistsNote}</p>}
          {specialists && specialists.length > 0 && (
            <ul className="mt-3 divide-y divide-cardline">
              {specialists.map((s, i) => (
                <li key={i} className="py-3">
                  <p className="font-medium text-ink">{s.name}</p>
                  <p className="text-sm text-muted">{s.address}</p>
                  {s.rating && <p className="text-xs text-amber mt-0.5">★ {s.rating}</p>}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      {result.unmatched_symptoms.length > 0 && (
        <p className="text-xs text-muted mt-6">
          Note: we couldn't confidently match these to our symptom list —{" "}
          {result.unmatched_symptoms.join(", ")}.
        </p>
      )}

      <div className="mt-8">
        <DisclaimerBanner />
      </div>
    </div>
  );
}
