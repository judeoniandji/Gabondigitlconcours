import React, { useState } from 'react';

export default function Navbar() {
  const [open, setOpen] = useState(false);
  const toggle = () => setOpen(!open);
  const logout = () => {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    window.location.href = '/';
  };
  return (
    <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',padding:'0.75em 1em',background:'#222',color:'#fff'}}>
      <div style={{fontWeight:'bold'}}>Digital Concours Admin</div>
      <div style={{position:'relative'}}>
        <button onClick={toggle} style={{background:'#444',color:'#fff',border:'none',padding:'0.5em 1em',borderRadius:4}}>Menu Admin ▾</button>
        {open && (
          <div style={{position:'absolute',right:0,top:'2.5em',background:'#fff',color:'#000',border:'1px solid #ccc',borderRadius:4,minWidth:260,boxShadow:'0 2px 8px #0002',zIndex:1000}}>
            <div style={{padding:'0.5em 1em',fontWeight:'bold',borderBottom:'1px solid #eee'}}>Frontend</div>
            <a href="/dashboard" style={{display:'block',padding:'0.5em 1em',textDecoration:'none',color:'#000'}}>Tableau de bord (Concours)</a>
            <a href="/admin-routes" style={{display:'block',padding:'0.5em 1em',textDecoration:'none',color:'#000'}}>Explorateur API Admin</a>
            <a href="/sessions" style={{display:'block',padding:'0.5em 1em',textDecoration:'none',color:'#000'}}>Gestion des sessions</a>
            <a href="/profiles" style={{display:'block',padding:'0.5em 1em',textDecoration:'none',color:'#000'}}>Gestion des profils</a>
            <a href="/logout" style={{display:'block',padding:'0.5em 1em',textDecoration:'none',color:'#000'}}>Déconnexion utilisateurs</a>
            <a href="/register" style={{display:'block',padding:'0.5em 1em',textDecoration:'none',color:'#000'}}>Inscription utilisateur</a>
            <a href="/suivi" style={{display:'block',padding:'0.5em 1em',textDecoration:'none',color:'#000'}}>Suivi de dossier</a>
            <a href="/paiement" style={{display:'block',padding:'0.5em 1em',textDecoration:'none',color:'#000'}}>Paiement Airtel</a>
            <a href="/candidat" style={{display:'block',padding:'0.5em 1em',textDecoration:'none',color:'#000'}}>Portail Candidat</a>
            <a href="/jury" style={{display:'block',padding:'0.5em 1em',textDecoration:'none',color:'#000'}}>Portail Jury</a>
            <a href="/secretaire" style={{display:'block',padding:'0.5em 1em',textDecoration:'none',color:'#000'}}>Portail Secrétaire</a>
            <a href="/roles" style={{display:'block',padding:'0.5em 1em',textDecoration:'none',color:'#000'}}>Choisir un espace</a>
            <div style={{padding:'0.5em 1em',fontWeight:'bold',borderTop:'1px solid #eee',borderBottom:'1px solid #eee'}}>Connexions</div>
            <a href="/login/candidat" style={{display:'block',padding:'0.5em 1em',textDecoration:'none',color:'#000'}}>Connexion Candidat</a>
            <a href="/login/jury" style={{display:'block',padding:'0.5em 1em',textDecoration:'none',color:'#000'}}>Connexion Jury</a>
            <a href="/login/secretaire" style={{display:'block',padding:'0.5em 1em',textDecoration:'none',color:'#000'}}>Connexion Secrétaire</a>
            <a href="/login/gestion" style={{display:'block',padding:'0.5em 1em',textDecoration:'none',color:'#000'}}>Connexion Gestion</a>
            <a href="/login/correcteur" style={{display:'block',padding:'0.5em 1em',textDecoration:'none',color:'#000'}}>Connexion Correcteur</a>
            <a href="/login/president" style={{display:'block',padding:'0.5em 1em',textDecoration:'none',color:'#000'}}>Connexion Président</a>
            <a href="/bugs" style={{display:'block',padding:'0.5em 1em',textDecoration:'none',color:'#000'}}>Suivi des bugs</a>
            <div style={{padding:'0.5em 1em',fontWeight:'bold',borderTop:'1px solid #eee',borderBottom:'1px solid #eee'}}>Backend</div>
            <a href="http://127.0.0.1:8000/admin/" target="_blank" rel="noreferrer" style={{display:'block',padding:'0.5em 1em',textDecoration:'none',color:'#000'}}>Django Admin</a>
            <a href="http://127.0.0.1:8000/swagger/" target="_blank" rel="noreferrer" style={{display:'block',padding:'0.5em 1em',textDecoration:'none',color:'#000'}}>Swagger API</a>
            <a href="http://127.0.0.1:8000/api/users/users/" target="_blank" rel="noreferrer" style={{display:'block',padding:'0.5em 1em',textDecoration:'none',color:'#000'}}>API Utilisateurs</a>
            <a href="http://127.0.0.1:8000/api/concours/concours/" target="_blank" rel="noreferrer" style={{display:'block',padding:'0.5em 1em',textDecoration:'none',color:'#000'}}>API Concours</a>
            <a href="http://127.0.0.1:8000/api/concours/dossiers/" target="_blank" rel="noreferrer" style={{display:'block',padding:'0.5em 1em',textDecoration:'none',color:'#000'}}>API Dossiers</a>
            <a href="http://127.0.0.1:8000/api/concours/resultats/" target="_blank" rel="noreferrer" style={{display:'block',padding:'0.5em 1em',textDecoration:'none',color:'#000'}}>API Résultats</a>
            <a href="http://127.0.0.1:8000/api/payments/paiements/" target="_blank" rel="noreferrer" style={{display:'block',padding:'0.5em 1em',textDecoration:'none',color:'#000'}}>API Paiements</a>
            <a href="http://127.0.0.1:8000/api/notifications/notifications/" target="_blank" rel="noreferrer" style={{display:'block',padding:'0.5em 1em',textDecoration:'none',color:'#000'}}>API Notifications</a>
            <div style={{borderTop:'1px solid #eee'}}>
              <button onClick={logout} style={{width:'100%',padding:'0.5em 1em',background:'#d9534f',color:'#fff',border:'none',borderRadius:0}}>Se déconnecter</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}