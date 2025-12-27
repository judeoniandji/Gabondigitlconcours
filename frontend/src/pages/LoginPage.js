import React, { useState } from 'react';
import { login, register } from '../services/auth';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);

  const handleLogin = async e => {
    e.preventDefault();
    try {
      await login(email, password);
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
    <div style={{maxWidth:400,margin:'auto',padding:'2em'}}>
      <h2>Connexion</h2>
      <form onSubmit={handleLogin}>
        <input type="email" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} required style={{width:'100%',padding:'0.5em',marginBottom:'1em'}} />
        <input type="password" placeholder="Mot de passe" value={password} onChange={e=>setPassword(e.target.value)} required style={{width:'100%',padding:'0.5em',marginBottom:'1em'}} />
        <button type="submit" style={{width:'100%',padding:'0.7em',background:'#007bff',color:'#fff',border:'none',borderRadius:'4px'}}>Se connecter</button>
      </form>
      {error !== null && error !== '' && <div style={{color:'red',marginTop:'1em'}}>{error}</div>}
    </div>
  );
}
