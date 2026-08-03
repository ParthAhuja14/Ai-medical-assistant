import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { diagnosisService } from "../services/diagnosisService";
import SymptomPicker from "../components/SymptomPicker";
import DisclaimerBanner from "../components/DisclaimerBanner";
import PulseDivider from "../components/PulseDivider";

export default function SymptomChecker() {
  const navigate = useNavigate();
  const [allSymptoms, setAllSymptoms] = useState([]);
  const [selected, setSelected] = useState([]);
  const [freeText, setFreeText] = useState("");
  const [age, setAge] = useState("");
  const [sex, setSex] = useState("");
  const [durationDays, setDurationDays] = useState("");
  const [severity, setSeverity] = useState("mild");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [coords, setCoords] = useState(null);

  useEffect(() => {
    diagnosisService.listSymptoms().then(({ data }) => setAllSymptoms(data.symptoms));

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => setCoords({ latitude: pos.coords.latitude, longitude: pos.coords.longitude }),
        () => setCoords(null)
      );
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (selected.length === 0 && !freeText.trim()) {
      setError("Please select at least one symptom or describe how you're feeling.");
      return;
    }
    setError("");
    setLoading(true);
    try {
      const { data } = await diagnosisService.submit({
        symptoms: selected,
        free_text: freeText || null,
        age: age ? parseInt(age, 10) : null,
        sex: sex || null,
        duration_days: durationDays ? parseInt(durationDays, 10) : null,
        severity,
        latitude: coords?.latitude,
        longitude: coords?.longitude,
      });
      navigate("/results", { state: { result: data } });
    } catch (err) {
      setError(err.response?.data?.detail || "Something went wrong analyzing your symptoms.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto px-6 py-12">
      <h1 className="font-display text-3xl text-ink">How are you feeling?</h1>
      <p className="text-muted mt-2 leading-relaxed">
        Select your symptoms below, or describe them in your own words. Our model will
        compare them against thousands of clinical cases to suggest possible conditions.
      </p>
      <PulseDivider />

      <form onSubmit={handleSubmit} className="mt-6 space-y-6">
        <div>
          <label className="block text-sm font-medium text-ink mb-2">Symptoms</label>
          <SymptomPicker allSymptoms={allSymptoms} selected={selected} onChange={setSelected} />
        </div>

        <div>
          <label className="block text-sm font-medium text-ink mb-2">
            Anything else you'd like to describe? <span className="text-muted font-normal">(optional)</span>
          </label>
          <textarea
            value={freeText}
            onChange={(e) => setFreeText(e.target.value)}
            rows={3}
            placeholder="e.g. It started three days ago and gets worse at night…"
            className="w-full px-4 py-3 rounded-lg border border-cardline focus:border-teal transition-colors resize-none"
          />
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div>
            <label className="block text-xs font-medium text-muted mb-1.5">Age</label>
            <input
              type="number"
              min={0}
              max={120}
              value={age}
              onChange={(e) => setAge(e.target.value)}
              className="w-full px-3 py-2 rounded-lg border border-cardline focus:border-teal transition-colors"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-muted mb-1.5">Sex</label>
            <select
              value={sex}
              onChange={(e) => setSex(e.target.value)}
              className="w-full px-3 py-2 rounded-lg border border-cardline focus:border-teal transition-colors bg-panel"
            >
              <option value="">—</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div>
            <label className="block text-xs font-medium text-muted mb-1.5">Days present</label>
            <input
              type="number"
              min={0}
              value={durationDays}
              onChange={(e) => setDurationDays(e.target.value)}
              className="w-full px-3 py-2 rounded-lg border border-cardline focus:border-teal transition-colors"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-muted mb-1.5">Severity</label>
            <select
              value={severity}
              onChange={(e) => setSeverity(e.target.value)}
              className="w-full px-3 py-2 rounded-lg border border-cardline focus:border-teal transition-colors bg-panel"
            >
              <option value="mild">Mild</option>
              <option value="moderate">Moderate</option>
              <option value="severe">Severe</option>
            </select>
          </div>
        </div>

        {error && <p className="text-sm text-alert">{error}</p>}

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-teal hover:bg-teal-dark text-white font-medium py-3 rounded-lg transition-colors disabled:opacity-60"
        >
          {loading ? "Analyzing symptoms…" : "Analyze my symptoms"}
        </button>

        <DisclaimerBanner />
      </form>
    </div>
  );
}
