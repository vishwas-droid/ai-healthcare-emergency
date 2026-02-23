type Props = {
  severity: string;
  score?: number;
};

const severityStyles: Record<string, string> = {
  LOW: "bg-emerald-100 text-emerald-700",
  MODERATE: "bg-amber-100 text-amber-800",
  HIGH: "bg-orange-100 text-orange-700",
  CRITICAL: "bg-rose-100 text-rose-700",
};

export function SeverityBadge({ severity, score }: Props) {
  const key = severity.toUpperCase();
  const style = severityStyles[key] || "bg-slate-100 text-slate-700";
  return (
    <span className={`inline-flex items-center gap-2 rounded-full px-3 py-1 text-xs font-semibold ${style}`}>
      {key}
      {typeof score === "number" && <span className="rounded-full bg-white/70 px-2 py-0.5 text-[10px]">{score}</span>}
    </span>
  );
}
