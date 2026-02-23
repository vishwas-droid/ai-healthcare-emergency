export type Analytics = {
  average_fee_per_city: { city: string; average_fee: number }[];
  fastest_ambulance_per_city: { city: string; provider_name: string; response_time_minutes: number }[];
  most_experienced_doctor_per_city: { city: string; doctor_name: string; experience_years: number }[];
  demand_category_analysis: { category: string; demand_count: number }[];
  demand_by_city: { city: string; demand_count: number }[];
};
