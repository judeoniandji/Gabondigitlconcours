import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import RegisterPage from './pages/RegisterPage';
import PaiementPage from './pages/PaiementPage';
import SuiviDossierPage from './pages/SuiviDossierPage';

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/paiement" element={<PaiementPage />} />
        <Route path="/suivi" element={<SuiviDossierPage />} />
      </Routes>
    </Router>
  );
}
