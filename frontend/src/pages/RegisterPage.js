import React, { useState } from 'react';
import { register } from '../services/auth';

export default function RegisterPage() {
  const [form, setForm] = useState({ email: '', username: '', password: '', telephone: '', role: 'candidat', nom_complet: '', date_naissance: '', lieu_naissance: '', ville_naissance: '', adresse: '' });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);
  const [fieldErrors, setFieldErrors] = useState({ email: '', username: '', password: '', telephone: '' });

  const validateMsisdnGabon = (value) => {
    if (!value) return '';
    const v = String(value).replace(/\s+/g, '');
    if (v.startsWith('+')) {
      return /^\+241\d{8}$/.test(v) ? '' : 'Format attendu: +241 suivi de 8 chiffres';
    }
    return /^\d{8}$/.test(v) ? '' : 'Format attendu: 8 chiffres (ex: 06234567)';
  };

  const validateField = (name, value) => {
    if (name === 'email') {
      const ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
      return ok ? '' : 'Email invalide';
    }
    if (name === 'username') {
      return value ? '' : "Nom d'utilisateur requis";
    }
    if (name === 'password') {
      return value && value.length >= 6 ? '' : 'Mot de passe trop court';
    }
    if (name === 'telephone') {
      return validateMsisdnGabon(value);
    }
    return '';
  };

  const handleChange = e => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
    const err = validateField(name, value);
    setFieldErrors({ ...fieldErrors, [name]: err });
  };

  const handleRegister = async e => {
    e.preventDefault();
    try {
      setLoading(true);
      await register(form);
      setSuccess(true);
      setError('');
      setLoading(false);
    } catch (err) {
      let msg = "Erreur lors de l'inscription";
      try {
        if (err.response && err.response.data) {
          const data = err.response.data;
          if (typeof data === 'string') msg = data;
          else {
            const values = Object.values(data);
            if (values.length > 0) msg = String(values[0]);
          }
        }
      } catch {}
      setError(msg);
      setLoading(false);
    }
  };

  if (success) return <div style={{padding:'2em'}}>Inscription réussie ! Vous pouvez vous connecter.</div>;

  return (
    <div style={{minHeight:'100vh',display:'flex',alignItems:'center',justifyContent:'center',background:'linear-gradient(135deg,#0d6efd 0%,#00b894 100%)'}}>
      <div style={{width:'100%',maxWidth:520,background:'#fff',borderRadius:16,boxShadow:'0 16px 40px #0002',overflow:'hidden'}}>
        <div style={{padding:'1.25em 1.5em',background:'#f7f9fc',display:'flex',alignItems:'center',gap:'0.75em',justifyContent:'space-between'}}>
          <div style={{display:'flex',alignItems:'center',gap:'0.75em'}}>
            <div style={{width:36,height:36,borderRadius:8,background:'#0d6efd'}} />
            <div style={{fontWeight:800,fontSize:18}}>République Gabonaise</div>
          </div>
          <div style={{color:'#667085',fontSize:13}}>Plateforme officielle des concours administratifs</div>
        </div>
        <div style={{padding:'1.75em 1.5em'}}>
          <div style={{marginBottom:'1em'}}>
            <div style={{fontSize:26,fontWeight:800}}>Inscription Candidat</div>
            <div style={{color:'#666'}}>Créez votre compte pour postuler</div>
          </div>
          <form onSubmit={handleRegister}>
            <div style={{display:'grid',gap:'0.85em'}}>
              <input name="email" type="email" placeholder="Email" value={form.email} onChange={handleChange} required style={{padding:'1em',border:'1px solid #e4e7ec',borderRadius:10,outline:'none'}} />
              {fieldErrors.email && <div style={{color:'#b00020',fontSize:13}}>{fieldErrors.email}</div>}
              <input name="username" placeholder="Nom d'utilisateur" value={form.username} onChange={handleChange} required style={{padding:'1em',border:'1px solid #e4e7ec',borderRadius:10,outline:'none'}} />
              {fieldErrors.username && <div style={{color:'#b00020',fontSize:13}}>{fieldErrors.username}</div>}
              <input name="password" type="password" placeholder="Mot de passe (min. 6 caractères)" value={form.password} onChange={handleChange} required style={{padding:'1em',border:'1px solid #e4e7ec',borderRadius:10,outline:'none'}} />
              {fieldErrors.password && <div style={{color:'#b00020',fontSize:13}}>{fieldErrors.password}</div>}
              <input name="telephone" placeholder="Téléphone" value={form.telephone} onChange={handleChange} style={{padding:'1em',border:'1px solid #e4e7ec',borderRadius:10,outline:'none'}} />
              {fieldErrors.telephone ? <div style={{color:'#b00020',fontSize:13}}>{fieldErrors.telephone}</div> : <div style={{color:'#667085',fontSize:12}}>Exemples: 06234567 ou +24162345678</div>}
              <input name="nom_complet" placeholder="Nom complet" value={form.nom_complet} onChange={handleChange} style={{padding:'1em',border:'1px solid #e4e7ec',borderRadius:10,outline:'none'}} />
              <input name="date_naissance" type="date" placeholder="Date de naissance" value={form.date_naissance} onChange={handleChange} style={{padding:'1em',border:'1px solid #e4e7ec',borderRadius:10,outline:'none'}} />
              <input name="lieu_naissance" placeholder="Lieu de naissance" value={form.lieu_naissance} onChange={handleChange} style={{padding:'1em',border:'1px solid #e4e7ec',borderRadius:10,outline:'none'}} />
              <input name="ville_naissance" placeholder="Ville de naissance" value={form.ville_naissance} onChange={handleChange} style={{padding:'1em',border:'1px solid #e4e7ec',borderRadius:10,outline:'none'}} />
              <input name="adresse" placeholder="Adresse" value={form.adresse} onChange={handleChange} style={{padding:'1em',border:'1px solid #e4e7ec',borderRadius:10,outline:'none'}} />
              <button type="submit" disabled={loading || !form.email || !form.username || !form.password || form.password.length < 6 || !!fieldErrors.email || !!fieldErrors.username || !!fieldErrors.password || !!fieldErrors.telephone} style={{padding:'1em',background: loading ? '#6c757d' : '#28a745',color:'#fff',border:'none',borderRadius:10,fontWeight:700,opacity: loading ? 0.8 : 1}}>S'inscrire</button>
            </div>
          </form>
          {error && <div style={{color:'#b00020',marginTop:'1em'}}>{error}</div>}
          <div style={{marginTop:'1.25em',display:'flex',justifyContent:'space-between',alignItems:'center'}}>
            <a href="/" style={{textDecoration:'none',color:'#0d6efd',fontWeight:700}}>Retour à la connexion</a>
            <a href="http://127.0.0.1:8000/swagger/" target="_blank" rel="noreferrer" style={{textDecoration:'none',color:'#6c757d'}}>Besoin d'aide ?</a>
          </div>
        </div>
      </div>
    </div>
  );
}
