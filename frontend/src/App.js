import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import RegisterPage from './pages/RegisterPage';
import PaiementPage from './pages/PaiementPage';
import SuiviDossierPage from './pages/SuiviDossierPage';
import Navbar from './components/Navbar';
import api from './services/api';
import AdminRoutesPage from './pages/AdminRoutesPage';
import CandidatePortalPage from './pages/CandidatePortalPage';
import JuryPortalPage from './pages/JuryPortalPage';
import SecretairePortalPage from './pages/SecretairePortalPage';
import RoleSelectorPage from './pages/RoleSelectorPage';
import SessionsAdminPage from './pages/SessionsAdminPage';
import ProfilesAdminPage from './pages/ProfilesAdminPage';
import LogoutUsersAdminPage from './pages/LogoutUsersAdminPage';
import LoginCandidatePage from './pages/LoginCandidatePage';
import LoginJuryPage from './pages/LoginJuryPage';
import LoginSecretairePage from './pages/LoginSecretairePage';
import LoginGestionPage from './pages/LoginGestionPage';
import LoginCorrecteurPage from './pages/LoginCorrecteurPage';
import LoginPresidentPage from './pages/LoginPresidentPage';
import BugTrackerAdminPage from './pages/BugTrackerAdminPage';

function AdminNavbarWrapper() {
  const [show, setShow] = useState(false);
  useEffect(() => {
    const access = localStorage.getItem('access');
    if (!access) return;
    api.get('users/me/').then(res => {
      const u = res.data;
      if (u.is_staff || u.is_superuser) setShow(true);
    }).catch(() => {});
  }, []);
  return show ? <Navbar /> : null;
}

export default function App() {
  return (
    <Router>
      <AdminNavbarWrapper />
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/paiement" element={<PaiementPage />} />
        <Route path="/suivi" element={<SuiviDossierPage />} />
        <Route path="/admin-routes" element={<AdminRoutesPage />} />
        <Route path="/candidat" element={<CandidatePortalPage />} />
        <Route path="/jury" element={<JuryPortalPage />} />
        <Route path="/secretaire" element={<SecretairePortalPage />} />
        <Route path="/roles" element={<RoleSelectorPage />} />
        <Route path="/sessions" element={<SessionsAdminPage />} />
        <Route path="/profiles" element={<ProfilesAdminPage />} />
        <Route path="/logout" element={<LogoutUsersAdminPage />} />
        <Route path="/login/candidat" element={<LoginCandidatePage />} />
        <Route path="/login/jury" element={<LoginJuryPage />} />
        <Route path="/login/secretaire" element={<LoginSecretairePage />} />
        <Route path="/login/gestion" element={<LoginGestionPage />} />
        <Route path="/login/correcteur" element={<LoginCorrecteurPage />} />
        <Route path="/login/president" element={<LoginPresidentPage />} />
        <Route path="/bugs" element={<BugTrackerAdminPage />} />
      </Routes>
    </Router>
  );
}
