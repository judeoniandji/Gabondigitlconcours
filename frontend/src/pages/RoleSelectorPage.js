import React, { useEffect, useState } from 'react';
import api from '../services/api';

export default function RoleSelectorPage() {
  const [me, setMe] = useState(null);
  useEffect(() => {
    const access = localStorage.getItem('access');
    if (!access) { window.location.href = '/'; return; }
    const load = async () => {
      try {
        const res = await api.get('users/me/');
        setMe(res.data);
      } catch {}
    };
    load();
  }, []);
  const go = (path) => (window.location.href = path);
  const role = me?.role;
  const isAdmin = !!me?.is_staff || !!me?.is_superuser;
  return (
    <div style={{padding:'2em'}}>
      <h2>Choisir votre espace</h2>
      {me && (
        <div style={{marginBottom:'1em'}}>Connecté en tant que <strong>{me.username}</strong> — rôle: <strong>{role || 'n/a'}</strong>{isAdmin ? ' (admin)' : ''}</div>
      )}
      <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fill,minmax(240px,1fr))',gap:'1em'}}>
        <div style={{border:'1px solid #ddd',borderRadius:8,padding:'1em'}}>
          <h3>Candidat</h3>
          <p>Postuler, suivre dossiers, paiements.</p>
          <button onClick={()=>go('/candidat')} disabled={role!=='candidat'}>Accéder</button>
        </div>
        <div style={{border:'1px solid #ddd',borderRadius:8,padding:'1em'}}>
          <h3>Jury</h3>
          <p>Consulter dossiers, publier résultats.</p>
          <button onClick={()=>go('/jury')} disabled={!(role==='jury' || role==='gestionnaire' || isAdmin)}>Accéder</button>
        </div>
        <div style={{border:'1px solid #ddd',borderRadius:8,padding:'1em'}}>
          <h3>Secrétaire</h3>
          <p>Valider/rejeter dossiers, gestion opérationnelle.</p>
          <button onClick={()=>go('/secretaire')} disabled={!(role==='secretaire' || role==='gestionnaire' || isAdmin)}>Accéder</button>
        </div>
        <div style={{border:'1px solid #ddd',borderRadius:8,padding:'1em'}}>
          <h3>Gestion</h3>
          <p>Créer concours, explorer API, administration.</p>
          <button onClick={()=>go('/dashboard')} disabled={!(role==='gestionnaire' || isAdmin)}>Tableau de bord</button>
          <button onClick={()=>go('/admin-routes')} style={{marginLeft:'0.5em'}} disabled={!(role==='gestionnaire' || isAdmin)}>API Admin</button>
        </div>
      </div>
    </div>
  );
}