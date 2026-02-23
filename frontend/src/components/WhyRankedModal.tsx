import type { RankingExplain } from "../types/ranking";

type Props = {
  open: boolean;
  title: string;
  explanation: RankingExplain | null;
  onClose: () => void;
};

export function WhyRankedModal({ open, title, explanation, onClose }: Props) {
  if (!open || !explanation) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-6">
      <div className="w-full max-w-xl rounded-2xl bg-surface p-6 shadow-premium">
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-bold">{title}</h3>
          <button onClick={onClose} className="rounded-full border px-3 py-1 text-sm">Close</button>
        </div>
        <p className="mt-2 text-sm text-muted">AI Score: {explanation.score_total}</p>
        {explanation.why_ranked_1 && (
          <p className="mt-2 rounded-lg bg-rose-50 px-3 py-2 text-sm text-rose-700">{explanation.why_ranked_1}</p>
        )}
        <div className="mt-4 grid gap-2 sm:grid-cols-2">
          {Object.entries(explanation.breakdown).map(([key, value]) => (
            <div key={key} className="rounded-xl border px-3 py-2 text-sm">
              <p className="text-xs uppercase text-muted">{key.replace(/_/g, " ")}</p>
              <p className="text-lg font-semibold">{value}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
