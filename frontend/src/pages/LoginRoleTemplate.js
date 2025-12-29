import React, { useState } from 'react';
import { login } from '../services/auth';
import api from '../services/api';

export default function LoginRoleTemplate({ expectedRole, title, redirect }) {
  const [identifier, setIdentifier] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async e => {
    e.preventDefault();
    setError('');
    try {
      await login(identifier, password);
      const me = (await api.get('users/me/')).data;
      const role = me.role;
      const isAdmin = !!me.is_staff || !!me.is_superuser;
      if (expectedRole === 'gestionnaire') {
        if (isAdmin || role === 'gestionnaire') {
          window.location.href = redirect || '/dashboard';
          return;
        }
      } else if (role === expectedRole) {
        window.location.href = redirect || '/';
        return;
      }
      setError(`Ce compte n’a pas le rôle attendu. Rôle: ${role || 'n/a'}`);
    } catch (err) {
      let msg = 'Identifiants invalides';
      try {
        if (err.response && err.response.data) {
          const v = Object.values(err.response.data);
          if (v.length > 0) msg = String(v[0]);
        }
      } catch {}
      setError(msg);
    }
  };

  return (
    <div style={{minHeight:'100vh',display:'flex',alignItems:'center',justifyContent:'center',background:'#f5f7fb'}}>
      <div style={{width:'100%',maxWidth:440,padding:'2em',background:'#fff',borderRadius:12,boxShadow:'0 8px 24px #0001'}}>
        <div style={{marginBottom:'1em'}}>
          <div style={{fontSize:24,fontWeight:700}}>{title}</div>
          <div style={{color:'#666'}}>Connectez‑vous pour accéder à votre espace</div>
        </div>
        <form onSubmit={handleLogin}>
          <div style={{display:'grid',gap:'0.75em'}}>
            <input
              type="text"
              placeholder={expectedRole==='candidat' ? "Email ou nom d'utilisateur" : "Nom d'utilisateur ou email"}
              value={identifier}
              onChange={e=>setIdentifier(e.target.value)}
              style={{padding:'0.9em',border:'1px solid #ddd',borderRadius:8}}
              required
            />
            <input
              type="password"
              placeholder="Mot de passe"
              value={password}
              onChange={e=>setPassword(e.target.value)}
              style={{padding:'0.9em',border:'1px solid #ddd',borderRadius:8}}
              required
            />
            <button type="submit" style={{padding:'0.9em',background:'#0d6efd',color:'#fff',border:'none',borderRadius:8,fontWeight:600}}>Se connecter</button>
          </div>
        </form>
        {error && <div style={{color:'#b00020',marginTop:'1em'}}>{error}</div>}
        <div style={{marginTop:'1em'}}>
          <a href="/roles" style={{textDecoration:'none',color:'#0d6efd'}}>Choisir un autre espace</a>
        </div>
      </div>
    </div>
  );
}