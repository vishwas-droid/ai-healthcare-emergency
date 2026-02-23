import type { Ambulance } from "./ambulance";
import type { Doctor } from "./doctor";

export type RecommendResponse = {
  doctors: Doctor[];
  ambulances: Ambulance[];
  top_doctor_summary: string;
  top_ambulance_summary: string;
  final_recommendation: string;
};

export type TrackingStartResponse = {
  tracking_id: number;
  provider_type: string;
  provider_id: number;
  eta_seconds: number;
  status: string;
};

export type TrackingStatusResponse = {
  tracking_id: number;
  status: string;
  eta_seconds: number;
  progress_percent: number;
  simulated_location: {
    lat: number;
    lng: number;
  };
};
