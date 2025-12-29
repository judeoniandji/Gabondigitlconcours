import React, { useState } from 'react';
import api from '../services/api';

const ROUTES = [
  { label: 'Utilisateurs', path: 'users/users/' },
  { label: 'Activer utilisateur (PUT id/activate)', path: 'users/users/1/activate/' },
  { label: 'Candidats', path: 'users/candidats/' },
  { label: 'Gestionnaires', path: 'users/gestionnaires/' },
  { label: 'Concours', path: 'concours/concours/' },
  { label: 'Concours: publier (PUT id/publier)', path: 'concours/concours/1/publier/' },
  { label: 'Dossiers', path: 'concours/dossiers/' },
  { label: 'Résultats', path: 'concours/resultats/' },
  { label: 'Séries', path: 'concours/series/' },
  { label: 'Matières', path: 'concours/matieres/' },
  { label: 'Notes', path: 'concours/notes/' },
  { label: 'Classement série (GET id/classement)', path: 'concours/series/1/classement/' },
  { label: 'Paiements', path: 'payments/paiements/' },
  { label: 'Init Paiement Airtel (POST)', path: 'payments/paiements/airtel/' },
  { label: 'Notifications', path: 'notifications/notifications/' },
];

export default function AdminRoutesPage() {
  const [route, setRoute] = useState(ROUTES[0].path);
  const [method, setMethod] = useState('GET');
  const [body, setBody] = useState('');
  const [result, setResult] = useState('');
  const [error, setError] = useState('');

  const execute = async () => {
    setError('');
    setResult('');
    try {
      let res;
      if (method === 'GET') {
        res = await api.get(route);
      } else if (method === 'POST') {
        const data = body ? JSON.parse(body) : {};
        res = await api.post(route, data);
      } else if (method === 'PUT') {
        const data = body ? JSON.parse(body) : {};
        res = await api.put(route, data);
      } else if (method === 'DELETE') {
        res = await api.delete(route);
      } else {
        throw new Error('Méthode non supportée');
      }
      setResult(JSON.stringify(res.data, null, 2));
    } catch (e) {
      if (e.response && e.response.data) {
        setError(JSON.stringify(e.response.data, null, 2));
      } else {
        setError(String(e));
      }
    }
  };

  return (
    <div style={{padding:'2em'}}>
      <h2>Explorateur API Admin</h2>
      <p>Exécute des requêtes authentifiées contre l’API (JWT requis).</p>
      <div style={{display:'grid',gap:'0.75em',maxWidth:800}}>
        <div style={{display:'flex',gap:'0.5em'}}>
          <select value={route} onChange={e=>setRoute(e.target.value)} style={{flex:3}}>
            {ROUTES.map(r => (<option key={r.path} value={r.path}>{r.label} — {r.path}</option>))}
          </select>
          <select value={method} onChange={e=>setMethod(e.target.value)} style={{flex:1}}>
            <option>GET</option>
            <option>POST</option>
            <option>PUT</option>
            <option>DELETE</option>
          </select>
          <button onClick={execute} style={{flex:1}}>Exécuter</button>
        </div>
        {(method === 'POST' || method === 'PUT') && (
          <textarea placeholder="Corps JSON" value={body} onChange={e=>setBody(e.target.value)} rows={8} style={{width:'100%'}} />
        )}
        {error && (
          <div style={{color:'white',background:'#d9534f',padding:'0.75em',borderRadius:4}}>
            <div style={{fontWeight:'bold'}}>Erreur</div>
            <pre style={{whiteSpace:'pre-wrap'}}>{error}</pre>
          </div>
        )}
        {result && (
          <div style={{background:'#f8f9fa',padding:'0.75em',borderRadius:4}}>
            <div style={{fontWeight:'bold'}}>Résultat</div>
            <pre style={{whiteSpace:'pre-wrap'}}>{result}</pre>
          </div>
        )}
      </div>
    </div>
  );
}