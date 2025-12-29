import React, { useEffect, useState } from 'react';
import api from '../services/api';

export default function DashboardPage() {
  const [concours, setConcours] = useState([]);
  const [error, setError] = useState('');
  const [form, setForm] = useState({ nom: '', description: '', date_ouverture: '', date_fermeture: '', frais_inscription: '' });
  useEffect(() => {
    const token = localStorage.getItem('access');
    if (!token) {
      window.location.href = '/';
      return;
    }
    const load = async () => {
      try {
        const res = await api.get('concours/concours/');
        setConcours(res.data);
      } catch (e) {
        setError('Erreur de chargement');
      }
    };
    load();
  }, []);
  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });
  const handleCreate = async e => {
    e.preventDefault();
    try {
      await api.post('concours/concours/', form);
      const res = await api.get('concours/concours/');
      setConcours(res.data);
      setForm({ nom: '', description: '', date_ouverture: '', date_fermeture: '', frais_inscription: '' });
      setError('');
    } catch (e) {
      let msg = 'Création échouée';
      if (e.response && e.response.data) {
        try {
          msg = JSON.stringify(e.response.data);
        } catch {}
      }
      setError(msg);
    }
  };
  return (
    <div style={{padding:'2em'}}>
      <h2>Tableau de bord</h2>
      <p>Bienvenue sur votre espace de gestion des concours !</p>
      <div style={{marginTop:'1em'}}>
        <h3>Créer un concours</h3>
        <form onSubmit={handleCreate} style={{display:'grid',gap:'0.5em',maxWidth:500}}>
          <input name="nom" placeholder="Nom" value={form.nom} onChange={handleChange} required />
          <input name="description" placeholder="Description" value={form.description} onChange={handleChange} />
          <input name="date_ouverture" type="date" placeholder="Date ouverture" value={form.date_ouverture} onChange={handleChange} required />
          <input name="date_fermeture" type="date" placeholder="Date fermeture" value={form.date_fermeture} onChange={handleChange} required />
          <input name="frais_inscription" type="number" step="0.01" placeholder="Frais" value={form.frais_inscription} onChange={handleChange} required />
          <button type="submit">Créer</button>
        </form>
      </div>
      <div style={{marginTop:'2em'}}>
        <h3>Concours</h3>
        {error && <div style={{color:'red'}}>{error}</div>}
        <ul>
          {concours.map(c => (
            <li key={c.id}><strong>{c.nom}</strong> — {c.date_ouverture} → {c.date_fermeture} — {c.frais_inscription} XAF</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
