import React, { useEffect, useState } from 'react';
import api from '../services/api';

export default function SessionsAdminPage() {
  const [users, setUsers] = useState([]);
  const [status, setStatus] = useState('');
  const [filterRole, setFilterRole] = useState('');
  useEffect(() => {
    const access = localStorage.getItem('access');
    if (!access) { window.location.href = '/'; return; }
    const load = async () => {
      try {
        const res = await api.get('users/users/');
        setUsers(res.data);
      } catch (e) {
        setStatus('Erreur de chargement des utilisateurs');
      }
    };
    load();
  }, []);
  const disconnect = async (id) => {
    setStatus('Déconnexion en cours...');
    try {
      await api.post('users/logout_user/', { user_id: id });
      setStatus('Utilisateur déconnecté');
    } catch (e) {
      setStatus('Erreur de déconnexion');
    }
  };
  return (
    <div style={{padding:'2em'}}>
      <h2>Gestion des sessions</h2>
      {status && <div>{status}</div>}
      <div style={{margin:'1em 0'}}>
        <label>Filtrer par rôle: </label>
        <select value={filterRole} onChange={e=>setFilterRole(e.target.value)}>
          <option value="">Tous</option>
          <option value="candidat">Candidat</option>
          <option value="gestionnaire">Gestionnaire</option>
          <option value="jury">Jury</option>
          <option value="secretaire">Secrétaire</option>
          <option value="correcteur">Correcteur</option>
          <option value="president_jury">Président de jury</option>
        </select>
      </div>
      <table style={{width:'100%',borderCollapse:'collapse'}}>
        <thead>
          <tr>
            <th style={{borderBottom:'1px solid #ccc',textAlign:'left'}}>ID</th>
            <th style={{borderBottom:'1px solid #ccc',textAlign:'left'}}>Nom</th>
            <th style={{borderBottom:'1px solid #ccc',textAlign:'left'}}>Email</th>
            <th style={{borderBottom:'1px solid #ccc',textAlign:'left'}}>Rôle</th>
            <th style={{borderBottom:'1px solid #ccc',textAlign:'left'}}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.filter(u => !filterRole || u.role === filterRole).map(u => (
            <tr key={u.id}>
              <td>{u.id}</td>
              <td>{u.username}</td>
              <td>{u.email}</td>
              <td>{u.role || '—'}</td>
              <td>
                <button onClick={()=>disconnect(u.id)}>Déconnecter</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}