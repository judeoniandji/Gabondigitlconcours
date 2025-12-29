import React, { useEffect, useState } from 'react';
import api from '../services/api';

export default function LogoutUsersAdminPage() {
  const [users, setUsers] = useState([]);
  const [status, setStatus] = useState('');

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

  const logoutUser = async (id) => {
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
      <h2>Déconnexion des utilisateurs</h2>
      {status && <div>{status}</div>}
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
          {users.map(u => (
            <tr key={u.id}>
              <td>{u.id}</td>
              <td>{u.username}</td>
              <td>{u.email}</td>
              <td>{u.role || '—'}</td>
              <td>{u.is_active ? 'Oui' : 'Non'}</td>
              <td>
                <button onClick={()=>logoutUser(u.id)}>Déconnecter</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}