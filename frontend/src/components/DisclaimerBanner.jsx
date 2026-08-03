export default function DisclaimerBanner({ compact = false }) {
  if (compact) {
    return (
      <p className="text-xs text-muted leading-relaxed">
        For general information only — not a medical diagnosis. Always consult a licensed
        healthcare professional.
      </p>
    );
  }
  return (
    <div className="border border-amber-light bg-amber-light rounded-lg px-4 py-3 flex gap-3 items-start">
      <span className="text-amber mt-0.5 select-none" aria-hidden="true">⚕</span>
      <p className="text-sm text-ink/80 leading-relaxed">
        <strong className="font-semibold">This is not a medical diagnosis.</strong>{" "}
        Symptomatic gives general, AI-assisted information to help you decide what to do
        next. Always consult a licensed healthcare professional for anything you're
        concerned about, and seek emergency care immediately for severe or worsening symptoms.
      </p>
    </div>
  );
}
