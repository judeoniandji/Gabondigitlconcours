import React, { useState } from 'react';
import { register } from '../services/auth';

export default function RegisterPage() {
  const [form, setForm] = useState({ email: '', username: '', password: '', telephone: '' });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const handleRegister = async e => {
    e.preventDefault();
    try {
      await register(form);
      setSuccess(true);
      setError('');
    } catch (err) {
      setError("Erreur lors de l'inscription");
    }
  };

  if (success) return <div style={{padding:'2em'}}>Inscription réussie ! Vous pouvez vous connecter.</div>;

  return (
    <div style={{maxWidth:400,margin:'auto',padding:'2em'}}>
      <h2>Inscription</h2>
      <form onSubmit={handleRegister}>
        <input name="email" type="email" placeholder="Email" value={form.email} onChange={handleChange} required style={{width:'100%',padding:'0.5em',marginBottom:'1em'}} />
        <input name="username" placeholder="Nom d'utilisateur" value={form.username} onChange={handleChange} required style={{width:'100%',padding:'0.5em',marginBottom:'1em'}} />
        <input name="password" type="password" placeholder="Mot de passe" value={form.password} onChange={handleChange} required style={{width:'100%',padding:'0.5em',marginBottom:'1em'}} />
        <input name="telephone" placeholder="Téléphone" value={form.telephone} onChange={handleChange} style={{width:'100%',padding:'0.5em',marginBottom:'1em'}} />
        <button type="submit" style={{width:'100%',padding:'0.7em',background:'#28a745',color:'#fff',border:'none',borderRadius:'4px'}}>S'inscrire</button>
      </form>
      {error && <div style={{color:'red',marginTop:'1em'}}>{error}</div>}
    </div>
  );
}
