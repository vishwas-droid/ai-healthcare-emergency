export type TriageRequest = {
  complaint_text: string;
  location_city?: string;
  latitude?: number;
  longitude?: number;
  user_id?: string;
};

export type TriageResponse = {
  emergency_id: string;
  severity: string;
  severity_score: number;
  emergency_type: string;
  entities: {
    symptoms: string[];
    duration: string;
    vitals: { bp: string | null; hr: string | null; spo2: string | null };
    risk_factors: string[];
    medications: string[];
  };
  recommended: {
    doctor_specialty: string;
    ambulance_priority: string;
    hospital_type: string;
  };
  risk_flags: string[];
  escalation: { triggered: boolean; reason: string };
  confidence: number;
};
