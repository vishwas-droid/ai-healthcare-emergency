export type Hospital = {
  id: number;
  name: string;
  city: string;
  state: string;
  country: string;
  icu_beds_available: number;
  emergency_wait_minutes: number;
  success_rate: number;
  avg_cost_index: number;
  distance_km_estimate: number;
  latitude: number;
  longitude: number;
  phone_number: string;
  is_available: boolean;
  ai_score: number;
};
