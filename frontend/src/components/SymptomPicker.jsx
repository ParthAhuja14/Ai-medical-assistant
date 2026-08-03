import { useState, useMemo, useRef, useEffect } from "react";
import { X, Search } from "lucide-react";

function formatSymptomLabel(raw) {
  return raw.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

export default function SymptomPicker({ allSymptoms, selected, onChange }) {
  const [query, setQuery] = useState("");
  const [open, setOpen] = useState(false);
  const wrapperRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(e) {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const suggestions = useMemo(() => {
    if (!query.trim()) return [];
    const q = query.toLowerCase().replace(/\s+/g, "_");
    return allSymptoms
      .filter((s) => !selected.includes(s))
      .filter((s) => s.includes(q))
      .slice(0, 8);
  }, [query, allSymptoms, selected]);

  const addSymptom = (symptom) => {
    if (!selected.includes(symptom)) {
      onChange([...selected, symptom]);
    }
    setQuery("");
    setOpen(false);
  };

  const removeSymptom = (symptom) => {
    onChange(selected.filter((s) => s !== symptom));
  };

  return (
    <div className="w-full">
      <div ref={wrapperRef} className="relative">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted" />
          <input
            type="text"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setOpen(true);
            }}
            onFocus={() => setOpen(true)}
            placeholder="Search symptoms — e.g. headache, fatigue, joint pain"
            className="w-full pl-10 pr-4 py-3 rounded-lg border border-cardline bg-panel text-ink placeholder:text-muted/70 focus:border-teal transition-colors"
          />
        </div>

        {open && suggestions.length > 0 && (
          <ul className="absolute z-20 w-full mt-1 bg-panel border border-cardline rounded-lg shadow-card overflow-hidden max-h-64 overflow-y-auto">
            {suggestions.map((s) => (
              <li key={s}>
                <button
                  type="button"
                  onClick={() => addSymptom(s)}
                  className="w-full text-left px-4 py-2.5 hover:bg-teal-light text-sm text-ink transition-colors"
                >
                  {formatSymptomLabel(s)}
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>

      {selected.length > 0 && (
        <div className="flex flex-wrap gap-2 mt-4">
          {selected.map((s) => (
            <span
              key={s}
              className="inline-flex items-center gap-1.5 bg-teal-light text-teal-dark text-sm font-medium px-3 py-1.5 rounded-full"
            >
              {formatSymptomLabel(s)}
              <button
                type="button"
                onClick={() => removeSymptom(s)}
                aria-label={`Remove ${formatSymptomLabel(s)}`}
                className="hover:text-alert transition-colors"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
