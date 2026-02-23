export type BookingPayload = {
  provider_type: "doctor" | "ambulance";
  provider_id: number;
  city: string;
  user_name?: string;
  user_phone?: string;
  notes?: string;
};

export type Booking = {
  id: number;
  provider_type: string;
  provider_id: number;
  user_name: string;
  user_phone: string;
  city: string;
  status: string;
  notes: string;
  created_at: string;
};
