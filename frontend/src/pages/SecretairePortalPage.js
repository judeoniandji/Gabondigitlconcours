import React, { useEffect, useState } from 'react';
import api from '../services/api';

export default function SecretairePortalPage() {
  const [dossiers, setDossiers] = useState([]);
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
  const update = async (id, newStatut) => {
    setStatus('Mise à jour...');
    try {
      await api.put(`concours/dossiers/${id}/`, { statut: newStatut });
      const res = await api.get('concours/dossiers/');
      setDossiers(res.data);
      setStatus('Statut mis à jour');
    } catch (e) {
      setStatus('Erreur de mise à jour');
    }
  };
  return (
    <div style={{minHeight:'100vh',background:'#f5f7fb',padding:'2em'}}>
      <div style={{maxWidth:980,margin:'0 auto'}}>
        <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}>
          <div style={{fontSize:24,fontWeight:800}}>Espace Secrétariat</div>
          <div style={{color:'#667085'}}>Validation administrative</div>
        </div>
        {status && <div style={{marginTop:'0.75em',color:'#0d6efd'}}>{status}</div>}
        <div style={{background:'#fff',borderRadius:12,boxShadow:'0 8px 24px #0001',padding:'1em',marginTop:'1em'}}>
          <table style={{width:'100%',borderCollapse:'collapse'}}>
            <thead>
              <tr>
                <th style={{borderBottom:'1px solid #eee',textAlign:'left',padding:'0.6em'}}>ID</th>
                <th style={{borderBottom:'1px solid #eee',textAlign:'left',padding:'0.6em'}}>Concours</th>
                <th style={{borderBottom:'1px solid #eee',textAlign:'left',padding:'0.6em'}}>Candidat</th>
                <th style={{borderBottom:'1px solid #eee',textAlign:'left',padding:'0.6em'}}>Référence</th>
                <th style={{borderBottom:'1px solid #eee',textAlign:'left',padding:'0.6em'}}>Statut</th>
                <th style={{borderBottom:'1px solid #eee',textAlign:'left',padding:'0.6em'}}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {dossiers.map(d => (
                <tr key={d.id} style={{borderBottom:'1px solid #f5f7fb'}}>
                  <td style={{padding:'0.6em'}}>{d.id}</td>
                  <td style={{padding:'0.6em'}}>{d.concours}</td>
                  <td style={{padding:'0.6em'}}>{d.candidat}</td>
                  <td style={{padding:'0.6em'}}>{d.reference || '—'}</td>
                  <td style={{padding:'0.6em'}}>{d.statut}</td>
                  <td style={{padding:'0.6em'}}>
                    <button onClick={()=>update(d.id, 'valide')} style={{padding:'0.5em 0.8em',background:'#0d6efd',color:'#fff',border:'none',borderRadius:8}}>Valider</button>
                    <button onClick={()=>update(d.id, 'rejete')} style={{padding:'0.5em 0.8em',background:'#b00020',color:'#fff',border:'none',borderRadius:8,marginLeft:'0.5em'}}>Rejeter</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
