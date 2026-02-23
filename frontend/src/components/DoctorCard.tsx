import { Link } from "react-router-dom";

import type { Doctor } from "../types/doctor";

type Props = {
  doctor: Doctor;
  onTrack?: (doctor: Doctor) => void;
};

export function DoctorCard({ doctor, onTrack }: Props) {
  return (
    <article className="rounded-2xl bg-white p-5 shadow-premium">
      <div className="flex items-start gap-4">
        <img src={doctor.photo_url} alt={doctor.name} className="h-20 w-20 rounded-xl object-cover" />
        <div className="flex-1">
          <h3 className="text-xl font-bold">{doctor.name}</h3>
          <p className="text-sm text-slate-600">
            {doctor.category} | {doctor.qualification}
          </p>
          <p className="text-sm text-slate-600">
            {doctor.college} | {doctor.city}
          </p>
          <div className="mt-2 flex flex-wrap gap-2 text-xs">
            <span className="rounded-full bg-rose-100 px-2 py-1 font-semibold text-primary">AI Score {doctor.ai_score}</span>
            {doctor.verified_status && (
              <span className="rounded-full bg-emerald-100 px-2 py-1 font-semibold text-emerald-700">Verified</span>
            )}
            <span className="rounded-full bg-slate-100 px-2 py-1">{doctor.availability_status}</span>
          </div>
        </div>
      </div>
      <div className="mt-4 grid grid-cols-2 gap-2 text-sm text-slate-700">
        <p>Experience: {doctor.experience_years} yrs</p>
        <p>
          Rating: {doctor.rating} ({doctor.reviews_count})
        </p>
        <p>Fee: INR {doctor.consultation_fee}</p>
        <p>Response: {doctor.response_time_minutes} min</p>
        <p>Patients: {doctor.total_patients_served}</p>
        <p>Languages: {doctor.languages}</p>
      </div>
      <div className="mt-4 flex flex-wrap gap-2">
        <button className="rounded-lg border px-3 py-2 text-sm">View Profile</button>
        <Link to={`/chat/${doctor.id}`} className="rounded-lg bg-slate-900 px-3 py-2 text-sm text-white">
          Chat Now
        </Link>
        <a href={doctor.whatsapp_link} target="_blank" className="rounded-lg bg-green-600 px-3 py-2 text-sm text-white" rel="noreferrer">
          WhatsApp Direct
        </a>
        <button className="rounded-lg bg-primary px-3 py-2 text-sm text-white">Book Appointment</button>
        {onTrack && (
          <button onClick={() => onTrack(doctor)} className="rounded-lg border border-primary px-3 py-2 text-sm text-primary">
            Track Doctor
          </button>
        )}
      </div>
    </article>
  );
}
