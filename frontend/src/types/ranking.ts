import type { Ambulance } from "./ambulance";
import type { Doctor } from "./doctor";
import type { Hospital } from "./hospital";

export type RankingRequest = {
  emergency_id: string;
  budget: number;
  severity: string;
  location_city?: string;
  latitude?: number;
  longitude?: number;
  max_results?: number;
};

export type RankingExplain = {
  target_id: number;
  target_type: string;
  score_total: number;
  breakdown: Record<string, number>;
  why_ranked_1?: string | null;
};

export type DoctorRankingResponse = {
  doctors: Doctor[];
  explanations: RankingExplain[];
};

export type AmbulanceRankingResponse = {
  ambulances: Ambulance[];
  explanations: RankingExplain[];
};

export type HospitalRankingResponse = {
  hospitals: Hospital[];
  explanations: RankingExplain[];
};
