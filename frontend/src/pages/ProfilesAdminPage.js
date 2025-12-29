import React, { useEffect, useState } from 'react';
import api from '../services/api';

const ROLES = ['candidat','gestionnaire','jury','secretaire','correcteur','president_jury'];

export default function ProfilesAdminPage() {
  const [users, setUsers] = useState([]);
  const [status, setStatus] = useState('');
  const [newUser, setNewUser] = useState({ email:'', username:'', password:'', telephone:'', role:'candidat' });
  const [filterRole, setFilterRole] = useState('');
  const [telError, setTelError] = useState('');

  useEffect(() => {
    const access = localStorage.getItem('access');
    if (!access) { window.location.href = '/'; return; }
    load();
  }, []);

  const load = async () => {
    try {
      const res = await api.get('users/users/');
      setUsers(res.data);
    } catch (e) {
      setStatus('Erreur de chargement');
    }
  };

  const validateMsisdnGabon = (value) => {
    if (!value) return '';
    const v = String(value).replace(/\s+/g, '');
    if (v.startsWith('+')) {
      return /^\+241\d{8}$/.test(v) ? '' : 'Format: +241 suivi de 8 chiffres';
    }
    return /^\d{8}$/.test(v) ? '' : 'Format: 8 chiffres (ex: 06234567)';
  };

  const createUser = async () => {
    setStatus('Création en cours...');
    try {
      await api.post('users/users/', newUser);
      setNewUser({ email:'', username:'', password:'', telephone:'', role:'candidat' });
      await load();
      setStatus('Utilisateur créé');
    } catch (e) {
      setStatus('Erreur de création');
    }
  };

  const updateUser = async (id, patch) => {
    setStatus('Mise à jour...');
    try {
      await api.put(`users/users/${id}/`, patch);
      await load();
      setStatus('Mis à jour');
    } catch (e) {
      setStatus('Erreur de mise à jour');
    }
  };

  const deleteUser = async (id) => {
    setStatus('Suppression...');
    try {
      await api.delete(`users/users/${id}/`);
      await load();
      setStatus('Supprimé');
    } catch (e) {
      setStatus('Erreur de suppression');
    }
  };

  const activateUser = async (id) => {
    setStatus('Activation...');
    try {
      await api.put(`users/users/${id}/activate/`);
      await load();
      setStatus('Activé');
    } catch (e) {
      setStatus('Erreur d\'activation');
    }
  };

  return (
    <div style={{padding:'2em'}}>
      <h2>Gestion des profils</h2>
      {status && <div>{status}</div>}

      <div style={{border:'1px solid #eee',padding:'1em',borderRadius:8,marginBottom:'1em'}}>
        <h3>Créer un utilisateur</h3>
        <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fill,minmax(220px,1fr))',gap:'0.5em'}}>
          <input placeholder="Email" value={newUser.email} onChange={e=>setNewUser({...newUser,email:e.target.value})} />
          <input placeholder="Nom d'utilisateur" value={newUser.username} onChange={e=>setNewUser({...newUser,username:e.target.value})} />
          <input type="password" placeholder="Mot de passe" value={newUser.password} onChange={e=>setNewUser({...newUser,password:e.target.value})} />
          <div>
            <input placeholder="Téléphone (ex: 06234567 ou +24162345678)" value={newUser.telephone} onChange={e=>{ setNewUser({...newUser,telephone:e.target.value}); setTelError(validateMsisdnGabon(e.target.value)); }} style={{width:'100%'}} />
            {telError ? <div style={{color:'#b00020',fontSize:12,marginTop:'0.25em'}}>{telError}</div> : <div style={{color:'#667085',fontSize:12,marginTop:'0.25em'}}>Format Gabon: 8 chiffres ou +241 suivi de 8 chiffres</div>}
          </div>
          <select value={newUser.role} onChange={e=>setNewUser({...newUser,role:e.target.value})}>
            {ROLES.map(r=> (<option key={r} value={r}>{r}</option>))}
          </select>
        </div>
        <button onClick={createUser} disabled={!!telError} style={{marginTop:'0.5em'}}>Créer</button>
      </div>

      <div style={{margin:'1em 0'}}>
        <label>Filtrer par rôle: </label>
        <select value={filterRole} onChange={e=>setFilterRole(e.target.value)}>
          <option value="">Tous</option>
          {ROLES.map(r=> (<option key={r} value={r}>{r}</option>))}
        </select>
      </div>

      <table style={{width:'100%',borderCollapse:'collapse'}}>
        <thead>
          <tr>
            <th style={{borderBottom:'1px solid #ccc',textAlign:'left'}}>ID</th>
            <th style={{borderBottom:'1px solid #ccc',textAlign:'left'}}>Nom</th>
            <th style={{borderBottom:'1px solid #ccc',textAlign:'left'}}>Email</th>
            <th style={{borderBottom:'1px solid #ccc',textAlign:'left'}}>Rôle</th>
            <th style={{borderBottom:'1px solid #ccc',textAlign:'left'}}>Actif</th>
            <th style={{borderBottom:'1px solid #ccc',textAlign:'left'}}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.filter(u => !filterRole || u.role === filterRole).map(u => (
            <tr key={u.id}>
              <td>{u.id}</td>
              <td>{u.username}</td>
              <td>{u.email}</td>
              <td>
                <select value={u.role || ''} onChange={e=>updateUser(u.id, { role: e.target.value })}>
                  {ROLES.map(r=> (<option key={r} value={r}>{r}</option>))}
                </select>
              </td>
              <td>{u.is_active ? 'Oui' : 'Non'}</td>
              <td>
                {!u.is_active && <button onClick={()=>activateUser(u.id)}>Activer</button>}
                <button onClick={()=>deleteUser(u.id)} style={{marginLeft:'0.5em'}}>Supprimer</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
