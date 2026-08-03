export default function PulseDivider({ color = "#0E7C7B" }) {
  return (
    <div className="pulse-divider" aria-hidden="true">
      <svg viewBox="0 0 600 24" preserveAspectRatio="none">
        <path
          className="pulse-line-path"
          d="M0,12 L180,12 L200,2 L220,22 L240,4 L260,20 L280,12 L420,12 L440,4 L460,20 L480,12 L600,12"
          fill="none"
          stroke={color}
          strokeWidth="1.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    </div>
  );
}
