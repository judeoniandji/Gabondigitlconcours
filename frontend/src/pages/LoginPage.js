import React, { useState } from 'react';
import { login } from '../services/auth';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);

  const handleLogin = async e => {
    e.preventDefault();
    try {
      await login(username, password);
      window.location.href = '/dashboard';
    } catch (err) {
      let msg = 'Identifiants invalides';
      if (err.response && err.response.data && typeof err.response.data === 'object') {
        const values = Object.values(err.response.data);
        if (values.length > 0) msg = values[0];
      }
      setError(msg);
    }
  };

  return (
    <div style={{minHeight:'100vh',display:'flex',alignItems:'center',justifyContent:'center',background:'linear-gradient(135deg,#0d6efd 0%,#00b894 100%)'}}>
      <div style={{width:'100%',maxWidth:480,background:'#fff',borderRadius:16,boxShadow:'0 16px 40px #0002',overflow:'hidden'}}>
        <div style={{padding:'1.25em 1.5em',background:'#f7f9fc',display:'flex',alignItems:'center',gap:'0.75em',justifyContent:'space-between'}}>
          <div style={{display:'flex',alignItems:'center',gap:'0.75em'}}>
            <div style={{width:36,height:36,borderRadius:8,background:'#0d6efd'}} />
            <div style={{fontWeight:800,fontSize:18}}>République Gabonaise</div>
          </div>
          <div style={{color:'#667085',fontSize:13}}>Plateforme officielle des concours administratifs</div>
        </div>
        <div style={{padding:'1.75em 1.5em'}}>
          <div style={{marginBottom:'1em'}}>
            <div style={{fontSize:26,fontWeight:800}}>Espace de connexion sécurisé</div>
            <div style={{color:'#666'}}>Accédez à votre espace</div>
          </div>
          <form onSubmit={handleLogin}>
            <div style={{display:'grid',gap:'0.85em'}}>
              <div style={{display:'flex',alignItems:'center',gap:'0.6em',border:'1px solid #e4e7ec',borderRadius:10,padding:'0.6em 0.8em'}}>
                <span aria-hidden="true" style={{fontSize:18}}>👤</span>
                <input aria-label="Identifiant" type="text" placeholder="Identifiant (nom d'utilisateur ou email)" value={username} onChange={e=>setUsername(e.target.value)} required style={{flex:1,padding:'0.4em 0',border:'none',outline:'none'}} />
              </div>
              <div style={{display:'flex',alignItems:'center',gap:'0.6em',border:'1px solid #e4e7ec',borderRadius:10,padding:'0.6em 0.8em'}}>
                <span aria-hidden="true" style={{fontSize:18}}>🔒</span>
                <input aria-label="Mot de passe" type="password" placeholder="Mot de passe" value={password} onChange={e=>setPassword(e.target.value)} required style={{flex:1,padding:'0.4em 0',border:'none',outline:'none'}} />
              </div>
              <button type="submit" style={{padding:'1em',background:'#0d6efd',color:'#fff',border:'none',borderRadius:10,fontWeight:700,letterSpacing:0.2}}>Se connecter</button>
            </div>
          </form>
          {error !== null && error !== '' && <div style={{color:'#b00020',marginTop:'1em'}}>{error}</div>}
          <div style={{marginTop:'1.25em',display:'flex',justifyContent:'space-between',alignItems:'center'}}>
            <a href="/register" style={{textDecoration:'none',color:'#0d6efd',fontWeight:700}}>Créer un compte</a>
            <a href="http://127.0.0.1:8000/swagger/" target="_blank" rel="noreferrer" style={{textDecoration:'none',color:'#6c757d'}}>Besoin d'aide ?</a>
          </div>
          <div style={{marginTop:'1.5em'}}>
            <div style={{fontWeight:800,marginBottom:'0.5em'}}>Sélectionnez votre profil pour accéder à votre espace</div>
            <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(160px,1fr))',gap:'0.75em'}}>
              <a href="/login/candidat" style={{display:'block',padding:'0.9em',border:'1px solid #e4e7ec',borderRadius:12,textDecoration:'none',color:'#0d6efd',fontWeight:700,textAlign:'center',transition:'transform 150ms ease, box-shadow 150ms ease'}} aria-label="Connexion Candidat">🎓 Candidat</a>
              <a href="/login/jury" style={{display:'block',padding:'0.9em',border:'1px solid #e4e7ec',borderRadius:12,textDecoration:'none',color:'#0d6efd',fontWeight:700,textAlign:'center',transition:'transform 150ms ease, box-shadow 150ms ease'}} aria-label="Connexion Jury">🧑‍⚖️ Jury</a>
              <a href="/login/correcteur" style={{display:'block',padding:'0.9em',border:'1px solid #e4e7ec',borderRadius:12,textDecoration:'none',color:'#0d6efd',fontWeight:700,textAlign:'center',transition:'transform 150ms ease, box-shadow 150ms ease'}} aria-label="Connexion Correcteur">📝 Correcteur</a>
              <a href="/login/secretaire" style={{display:'block',padding:'0.9em',border:'1px solid #e4e7ec',borderRadius:12,textDecoration:'none',color:'#0d6efd',fontWeight:700,textAlign:'center',transition:'transform 150ms ease, box-shadow 150ms ease'}} aria-label="Connexion Secrétariat">🗂️ Secrétariat</a>
              <a href="/login/gestion" style={{display:'block',padding:'0.9em',border:'1px solid #e4e7ec',borderRadius:12,textDecoration:'none',color:'#0d6efd',fontWeight:700,textAlign:'center',transition:'transform 150ms ease, box-shadow 150ms ease'}} aria-label="Connexion Gestion">⚙️ Gestion</a>
              <a href="/login/president" style={{display:'block',padding:'0.9em',border:'1px solid #e4e7ec',borderRadius:12,textDecoration:'none',color:'#0d6efd',fontWeight:700,textAlign:'center',transition:'transform 150ms ease, box-shadow 150ms ease'}} aria-label="Connexion Président">👔 Président</a>
            </div>
            <div style={{marginTop:'0.75em',color:'#667085'}}>Vos données sont protégées</div>
          </div>
          <div style={{marginTop:'1.75em',borderTop:'1px solid #f0f2f5',paddingTop:'0.75em',color:'#667085',fontSize:12,textAlign:'center'}}>
            Plateforme officielle des concours administratifs · République Gabonaise<br />© 2025 – Accès sécurisé
          </div>
        </div>
      </div>
    </div>
  );
}
