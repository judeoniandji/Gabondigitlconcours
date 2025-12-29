import React, { useEffect, useState } from 'react';
import api from '../services/api';

export default function JuryPortalPage() {
  const [dossiers, setDossiers] = useState([]);
  const [note, setNote] = useState('');
  const [admis, setAdmis] = useState(false);
  const [selectedDossier, setSelectedDossier] = useState('');
  const [status, setStatus] = useState('');

  useEffect(() => {
    const access = localStorage.getItem('access');
    if (!access) { window.location.href = '/'; return; }
    const load = async () => {
      const res = await api.get('concours/dossiers/');
      setDossiers(res.data);
    };
    load();
  }, []);

  const publierResultat = async () => {
    if (!selectedDossier) return;
    setStatus('Publication...');
    try {
      await api.post('concours/resultats/', { dossier: selectedDossier, note: note || null, admis });
      await api.put(`concours/dossiers/${selectedDossier}/`, { statut: admis ? 'valide' : 'rejete' });
      setStatus('Résultat publié et dossier mis à jour');
    } catch (e) {
      setStatus('Erreur de publication');
    }
  };

  return (
    <div style={{minHeight:'100vh',background:'#f5f7fb',padding:'2em'}}>
      <div style={{maxWidth:980,margin:'0 auto'}}>
        <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}>
          <div style={{fontSize:24,fontWeight:800}}>Espace Jury</div>
          <div style={{color:'#667085'}}>Traitement confidentiel des dossiers</div>
        </div>
        <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:'1em',marginTop:'1em'}}>
          <div style={{background:'#fff',borderRadius:12,boxShadow:'0 8px 24px #0001',padding:'1em'}}>
            <div style={{fontWeight:700,marginBottom:'0.5em'}}>Publier un résultat</div>
            <div style={{display:'grid',gap:'0.75em',maxWidth:600}}>
              <select value={selectedDossier} onChange={e=>setSelectedDossier(e.target.value)} style={{padding:'0.7em',border:'1px solid #e4e7ec',borderRadius:10}}>
                <option value="">Sélectionner un dossier...</option>
                {dossiers.map(d => (<option key={d.id} value={d.id}>Dossier #{d.id} — Concours #{d.concours}</option>))}
              </select>
              <input type="number" step="0.01" placeholder="Note" value={note} onChange={e=>setNote(e.target.value)} style={{padding:'0.7em',border:'1px solid #e4e7ec',borderRadius:10}} />
              <label style={{display:'flex',alignItems:'center',gap:'0.5em'}}>
                <input type="checkbox" checked={admis} onChange={e=>setAdmis(e.target.checked)} /> Admis
              </label>
              <button onClick={publierResultat} style={{padding:'0.8em 1.2em',background:'#0d6efd',color:'#fff',border:'none',borderRadius:10,fontWeight:700}}>Publier le résultat</button>
              {status && <div style={{color:'#0d6efd'}}>{status}</div>}
            </div>
          </div>
          <div style={{background:'#fff',borderRadius:12,boxShadow:'0 8px 24px #0001',padding:'1em'}}>
            <div style={{fontWeight:700,marginBottom:'0.5em'}}>Tous les dossiers</div>
            <div style={{display:'grid',gap:'0.5em'}}>
              {dossiers.map(d => (<div key={d.id} style={{border:'1px solid #e4e7ec',borderRadius:10,padding:'0.7em'}}>#{d.id} — Statut: {d.statut} — Réf: {d.reference || '—'}</div>))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
