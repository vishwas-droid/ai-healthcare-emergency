export type Ambulance = {
  id: number;
  provider_name: string;
  city: string;
  state: string;
  vehicle_type: string;
  response_time_minutes: number;
  cost_per_km: number;
  base_price: number;
  availability_status: string;
  rating: number;
  verified_status: boolean;
  total_cases_handled: number;
  equipment_list: string;
  phone_number: string;
  whatsapp_link: string;
  ai_score: number;
};
