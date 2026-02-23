import { Navigate, Route, Routes } from "react-router-dom";

import { Layout } from "./components/Layout";
import { AdminPanel } from "./pages/AdminPanel";
import { AmbulancesPage } from "./pages/AmbulancesPage";
import { AnalyticsPage } from "./pages/AnalyticsPage";
import { ChatPage } from "./pages/ChatPage";
import { ComparePage } from "./pages/ComparePage";
import { DoctorsPage } from "./pages/DoctorsPage";
import { HomePage } from "./pages/HomePage";
import { HospitalsPage } from "./pages/HospitalsPage";
import { LiveTrackingPage } from "./pages/LiveTrackingPage";
import { TriagePage } from "./pages/TriagePage";

export function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<HomePage />} />
        <Route path="triage" element={<TriagePage />} />
        <Route path="doctors" element={<DoctorsPage />} />
        <Route path="ambulances" element={<AmbulancesPage />} />
        <Route path="hospitals" element={<HospitalsPage />} />
        <Route path="compare" element={<ComparePage />} />
        <Route path="analytics" element={<AnalyticsPage />} />
        <Route path="tracking" element={<LiveTrackingPage />} />
        <Route path="admin" element={<AdminPanel />} />
        <Route path="chat/:doctorId" element={<ChatPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
