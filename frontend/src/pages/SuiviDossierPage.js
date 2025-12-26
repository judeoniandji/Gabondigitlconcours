import React, { useState } from 'react';
import api from '../services/api';

export default function SuiviDossierPage() {
  const [reference, setReference] = useState('');
  const [dossier, setDossier] = useState(null);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    setError('');
    setDossier(null);
    try {
      const res = await api.get(`/concours/dossiers/?reference=${reference}`);
      if (res.data.length === 0) setError('Aucun dossier trouvé');
      else setDossier(res.data[0]);
    } catch (err) {
      setError('Erreur lors de la recherche');
    }
  };

  return (
    <div style={{maxWidth:400,margin:'auto',padding:'2em'}}>
      <h2>Suivi de dossier</h2>
      <input type="text" placeholder="Référence dossier" value={reference} onChange={e=>setReference(e.target.value)} style={{width:'100%',padding:'0.5em',marginBottom:'1em'}} />
      <button onClick={handleSearch} style={{width:'100%',padding:'0.7em',background:'#17a2b8',color:'#fff',border:'none',borderRadius:'4px'}}>Rechercher</button>
      {error && <div style={{color:'red',marginTop:'1em'}}>{error}</div>}
      {dossier && (
        <div style={{marginTop:'2em',background:'#f8f9fa',padding:'1em',borderRadius:'4px'}}>
          <div><strong>Statut:</strong> {dossier.statut}</div>
          <div><strong>Date de soumission:</strong> {dossier.date_soumission}</div>
          {/* Ajouter d'autres infos au besoin */}
        </div>
      )}
    </div>
  );
}
