export type BookingPayload = {
  provider_type: "doctor" | "ambulance";
  provider_id: number;
  city: string;
  user_name?: string;
  user_phone?: string;
  notes?: string;
  payment_method?: "COD" | "UPI" | "RAZORPAY";
  upi_id?: string;
  distance_km?: number;
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

export type BookingCheckoutResponse = {
  booking: Booking;
  tracking_id: number;
  eta_seconds: number;
  payment_method: string;
  payment_status: string;
  payment_amount: number;
  razorpay_checkout_url: string;
};

export type BookingTrackingResponse = {
  booking_id: number;
  booking_status: string;
  tracking_id: number;
  eta_seconds: number;
  progress_percent: number;
  timeline: { step: string; done: boolean }[];
  simulated_location: { lat: number; lng: number };
};
