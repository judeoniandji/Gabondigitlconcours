import React, { useEffect, useState } from 'react';
import api from '../services/api';

export default function BugTrackerAdminPage() {
  const [bugs, setBugs] = useState([]);
  const [status, setStatus] = useState('');
  const [form, setForm] = useState({ titre:'', description:'', severite:'mineur', environnement:'', etapes:'', module:'', chemins:'' });

  const load = async () => {
    setStatus('Chargement...');
    try {
      const res = await api.get('users/bugs/');
      setBugs(res.data);
      setStatus('');
    } catch (e) {
      setStatus('Erreur de chargement');
    }
  };

  useEffect(() => { load(); }, []);

  const createBug = async e => {
    e.preventDefault();
    setStatus('Création...');
    try {
      await api.post('users/bugs/', form);
      setForm({ titre:'', description:'', severite:'mineur', environnement:'', etapes:'', module:'', chemins:'' });
      await load();
      setStatus('Bug créé');
    } catch (e) {
      setStatus('Erreur de création');
    }
  };

  const changeStatus = async (id, statut) => {
    setStatus('Mise à jour...');
    try {
      await api.put(`users/bugs/${id}/change_status/`, { statut });
      await load();
      setStatus('Statut mis à jour');
    } catch (e) {
      setStatus('Erreur de mise à jour');
    }
  };

  const addComment = async (id, text) => {
    setStatus('Ajout commentaire...');
    try {
      await api.post('users/bug-events/', { bug: id, type: 'comment', detail: text });
      await load();
      setStatus('Commentaire ajouté');
    } catch (e) {
      setStatus('Erreur commentaire');
    }
  };

  return (
    <div style={{padding:'1em'}}>
      <h2>Suivi des bugs</h2>
      <div style={{marginBottom:'1em',color:'#666'}}>{status}</div>
      <form onSubmit={createBug} style={{display:'grid',gap:'0.5em',maxWidth:720,marginBottom:'1.5em'}}>
        <input value={form.titre} onChange={e=>setForm({...form,titre:e.target.value})} placeholder="Titre" style={{padding:'0.7em',border:'1px solid #ddd',borderRadius:6}} required />
        <textarea value={form.description} onChange={e=>setForm({...form,description:e.target.value})} placeholder="Description" rows={4} style={{padding:'0.7em',border:'1px solid #ddd',borderRadius:6}} required />
        <textarea value={form.etapes} onChange={e=>setForm({...form,etapes:e.target.value})} placeholder="Étapes pour reproduire" rows={3} style={{padding:'0.7em',border:'1px solid #ddd',borderRadius:6}} />
        <input value={form.environnement} onChange={e=>setForm({...form,environnement:e.target.value})} placeholder="Environnement" style={{padding:'0.7em',border:'1px solid #ddd',borderRadius:6}} />
        <div style={{display:'flex',gap:'0.5em'}}>
          <select value={form.severite} onChange={e=>setForm({...form,severite:e.target.value})} style={{padding:'0.7em',border:'1px solid #ddd',borderRadius:6}}>
            <option value="bloquant">Bloquant</option>
            <option value="majeur">Majeur</option>
            <option value="mineur">Mineur</option>
            <option value="cosmetique">Cosmétique</option>
          </select>
          <input value={form.module} onChange={e=>setForm({...form,module:e.target.value})} placeholder="Module" style={{flex:1,padding:'0.7em',border:'1px solid #ddd',borderRadius:6}} />
        </div>
        <textarea value={form.chemins} onChange={e=>setForm({...form,chemins:e.target.value})} placeholder="Fichiers/chemins impactés" rows={2} style={{padding:'0.7em',border:'1px solid #ddd',borderRadius:6}} />
        <button type="submit" style={{padding:'0.8em',background:'#0d6efd',color:'#fff',border:'none',borderRadius:6,fontWeight:600}}>Créer un bug</button>
      </form>

      <div style={{display:'grid',gap:'1em'}}>
        {bugs.map(b => (
          <div key={b.id} style={{border:'1px solid #eee',borderRadius:8,padding:'0.8em'}}>
            <div style={{display:'flex',justifyContent:'space-between'}}>
              <div style={{fontWeight:700}}>{b.titre}</div>
              <div style={{display:'flex',gap:'0.5em',alignItems:'center'}}>
                <span>Statut:</span>
                <select value={b.statut} onChange={e=>changeStatus(b.id, e.target.value)}>
                  <option value="ouvert">Ouvert</option>
                  <option value="en_cours">En cours</option>
                  <option value="corrige">Corrigé</option>
                  <option value="valide">Validé</option>
                  <option value="rejete">Rejeté</option>
                </select>
              </div>
            </div>
            <div style={{color:'#555',margin:'0.4em 0'}}>Sévérité: {b.severite} · Module: {b.module || '—'}</div>
            <div style={{margin:'0.4em 0'}}>{b.description}</div>
            {b.etapes && <div style={{whiteSpace:'pre-wrap',color:'#666'}}>Étapes: {b.etapes}</div>}
            {b.environnement && <div style={{color:'#666'}}>Env: {b.environnement}</div>}
            {b.chemins && <div style={{whiteSpace:'pre-wrap',color:'#666'}}>Chemins: {b.chemins}</div>}
            <div style={{marginTop:'0.6em'}}>
              <div style={{fontWeight:600}}>Historique</div>
              <div style={{display:'grid',gap:'0.25em'}}>
                {(b.events||[]).map(ev => (
                  <div key={ev.id} style={{fontSize:14,color:'#444'}}>• [{ev.type}] {ev.detail} ({new Date(ev.created_at).toLocaleString()})</div>
                ))}
              </div>
              <div style={{display:'flex',gap:'0.5em',marginTop:'0.5em'}}>
                <input placeholder="Ajouter un commentaire" style={{flex:1,padding:'0.6em',border:'1px solid #ddd',borderRadius:6}} onKeyDown={e=>{ if(e.key==='Enter'){ addComment(b.id, e.target.value); e.target.value=''; } }} />
                <button onClick={()=>{ const el = document.querySelector(`#cmt-${b.id}`); if(el){ addComment(b.id, el.value); el.value=''; } }} style={{padding:'0.6em 1em'}}>Envoyer</button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}