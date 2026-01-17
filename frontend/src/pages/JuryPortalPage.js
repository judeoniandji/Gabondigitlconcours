import React, { useEffect, useState } from 'react';
import api from '../services/api';

export default function JuryPortalPage() {
  const [user, setUser] = useState(null);
  const [concoursList, setConcoursList] = useState([]);
  const [seriesList, setSeriesList] = useState([]);
  const [matieresList, setMatieresList] = useState([]);
  
  const [selectedConcours, setSelectedConcours] = useState('');
  const [selectedSerie, setSelectedSerie] = useState('');
  const [selectedMatiere, setSelectedMatiere] = useState('');
  
  const [candidats, setCandidats] = useState([]);
  const [classement, setClassement] = useState(null);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState({}); // { [dossierId]: boolean }
  const [activeTab, setActiveTab] = useState('notes'); // 'notes' | 'deliberation'

  // Load initial data
  useEffect(() => {
    const load = async () => {
      try {
        const u = await api.get('users/me/');
        setUser(u.data);
        const c = await api.get('concours/concours/');
        setConcoursList(c.data);
        const s = await api.get('concours/series/');
        setSeriesList(s.data);
        const m = await api.get('concours/matieres/');
        setMatieresList(m.data);
      } catch (e) {
        console.error(e);
        window.location.href = '/login/jury';
      }
    };
    load();
  }, []);

  // Load candidates when Matiere is selected (Notes tab)
  useEffect(() => {
    if (activeTab === 'notes' && selectedMatiere) {
      const fetchCandidats = async () => {
        setLoading(true);
        try {
          const res = await api.get(`concours/matieres/${selectedMatiere}/candidats/`);
          // Add local state for note input
          const data = res.data.map(c => ({
            ...c,
            noteInput: c.note ? c.note.valeur : ''
          }));
          setCandidats(data);
        } catch (e) {
          console.error(e);
        } finally {
          setLoading(false);
        }
      };
      fetchCandidats();
    }
  }, [selectedMatiere, activeTab]);

  // Load ranking when Serie is selected (Deliberation tab)
  useEffect(() => {
    if (activeTab === 'deliberation' && selectedSerie) {
      const fetchClassement = async () => {
        setLoading(true);
        try {
          const res = await api.get(`concours/series/${selectedSerie}/classement/`);
          setClassement(res.data.classement);
        } catch (e) {
          console.error(e);
        } finally {
          setLoading(false);
        }
      };
      fetchClassement();
    }
  }, [selectedSerie, activeTab]);

  const handleNoteChange = (dossierId, value) => {
    setCandidats(prev => prev.map(c => 
      c.dossier_id === dossierId ? { ...c, noteInput: value } : c
    ));
  };

  const saveNote = async (candidat) => {
    if (!candidat.noteInput) return;
    setSaving(prev => ({ ...prev, [candidat.dossier_id]: true }));
    try {
      if (candidat.note) {
        // Update existing note
        await api.patch(`concours/notes/${candidat.note.id}/`, {
          valeur: candidat.noteInput
        });
      } else {
        // Create new note
        await api.post(`concours/notes/`, {
          matiere: selectedMatiere,
          valeur: candidat.noteInput,
          candidat_numero_input: candidat.candidat_numero
        });
      }
      // Refresh list to get updated note ID and status
      const res = await api.get(`concours/matieres/${selectedMatiere}/candidats/`);
      const data = res.data.map(c => ({
        ...c,
        noteInput: c.note ? c.note.valeur : ''
      }));
      setCandidats(data);
    } catch (e) {
      alert('Erreur lors de la sauvegarde: ' + (e.response?.data?.detail || e.message));
    } finally {
      setSaving(prev => ({ ...prev, [candidat.dossier_id]: false }));
    }
  };

  const validerNote = async (noteId) => {
    if (!window.confirm('Valider cette note ? Elle ne pourra plus être modifiée.')) return;
    try {
      await api.put(`concours/notes/${noteId}/valider/`);
      // Refresh
      const res = await api.get(`concours/matieres/${selectedMatiere}/candidats/`);
      const data = res.data.map(c => ({
        ...c,
        noteInput: c.note ? c.note.valeur : ''
      }));
      setCandidats(data);
    } catch (e) {
      alert('Erreur: ' + e.message);
    }
  };

  // Filter lists
  const filteredSeries = seriesList.filter(s => s.concours === Number(selectedConcours));
  const filteredMatieres = matieresList.filter(m => m.serie === Number(selectedSerie));

  if (!user) return <div>Chargement...</div>;

  return (
    <div style={{minHeight:'100vh',background:'#f5f7fb',padding:'2em'}}>
      <div style={{maxWidth:1200,margin:'0 auto'}}>
        <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:'2em'}}>
          <div>
            <div style={{fontSize:24,fontWeight:800}}>Espace Jury</div>
            <div style={{color:'#667085'}}>
              Connecté en tant que: <b>{user.role === 'president_jury' ? 'Président du Jury' : 'Correcteur'}</b>
            </div>
          </div>
          <button onClick={() => { localStorage.removeItem('access'); window.location.href = '/login/jury'; }} style={{background:'#fff',border:'1px solid #ddd',padding:'0.5em 1em',borderRadius:6}}>Déconnexion</button>
        </div>

        {/* Tabs for President */}
        {user.role === 'president_jury' && (
          <div style={{display:'flex',gap:'1em',marginBottom:'1.5em'}}>
            <button 
              onClick={() => setActiveTab('notes')}
              style={{
                padding:'0.7em 1.5em',borderRadius:8,border:'none',fontWeight:600,cursor:'pointer',
                background: activeTab === 'notes' ? '#0d6efd' : '#fff',
                color: activeTab === 'notes' ? '#fff' : '#444'
              }}
            >
              Saisie des notes
            </button>
            <button 
              onClick={() => setActiveTab('deliberation')}
              style={{
                padding:'0.7em 1.5em',borderRadius:8,border:'none',fontWeight:600,cursor:'pointer',
                background: activeTab === 'deliberation' ? '#0d6efd' : '#fff',
                color: activeTab === 'deliberation' ? '#fff' : '#444'
              }}
            >
              Délibération
            </button>
          </div>
        )}

        {/* Filters */}
        <div style={{background:'#fff',padding:'1.5em',borderRadius:12,boxShadow:'0 2px 8px #0001',marginBottom:'1.5em',display:'grid',gridTemplateColumns:'1fr 1fr 1fr',gap:'1em'}}>
          <div>
            <label style={{display:'block',marginBottom:5,fontWeight:600}}>Concours</label>
            <select value={selectedConcours} onChange={e => {setSelectedConcours(e.target.value); setSelectedSerie(''); setSelectedMatiere('');}} style={{width:'100%',padding:'0.6em',borderRadius:6,border:'1px solid #ddd'}}>
              <option value="">Sélectionner...</option>
              {concoursList.map(c => <option key={c.id} value={c.id}>{c.nom}</option>)}
            </select>
          </div>
          <div>
            <label style={{display:'block',marginBottom:5,fontWeight:600}}>Série</label>
            <select value={selectedSerie} onChange={e => {setSelectedSerie(e.target.value); setSelectedMatiere('');}} disabled={!selectedConcours} style={{width:'100%',padding:'0.6em',borderRadius:6,border:'1px solid #ddd'}}>
              <option value="">Sélectionner...</option>
              {filteredSeries.map(s => <option key={s.id} value={s.id}>{s.nom}</option>)}
            </select>
          </div>
          {activeTab === 'notes' && (
            <div>
              <label style={{display:'block',marginBottom:5,fontWeight:600}}>Matière</label>
              <select value={selectedMatiere} onChange={e => setSelectedMatiere(e.target.value)} disabled={!selectedSerie} style={{width:'100%',padding:'0.6em',borderRadius:6,border:'1px solid #ddd'}}>
                <option value="">Sélectionner...</option>
                {filteredMatieres.map(m => <option key={m.id} value={m.id}>{m.nom} (Coeff: {m.coefficient})</option>)}
              </select>
            </div>
          )}
        </div>

        {/* Notes View */}
        {activeTab === 'notes' && selectedMatiere && (
          <div style={{background:'#fff',padding:'1.5em',borderRadius:12,boxShadow:'0 2px 8px #0001'}}>
            <div style={{fontSize:18,fontWeight:700,marginBottom:'1em'}}>Saisie des notes</div>
            {loading ? <div>Chargement des candidats...</div> : (
              candidats.length === 0 ? <div>Aucun candidat trouvé pour cette matière.</div> : (
                <table style={{width:'100%',borderCollapse:'collapse'}}>
                  <thead>
                    <tr style={{textAlign:'left',borderBottom:'2px solid #eee'}}>
                      <th style={{padding:'1em'}}>Anonymat</th>
                      <th style={{padding:'1em'}}>Note / 20</th>
                      <th style={{padding:'1em'}}>État</th>
                      <th style={{padding:'1em'}}>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {candidats.map(c => (
                      <tr key={c.dossier_id} style={{borderBottom:'1px solid #eee'}}>
                        <td style={{padding:'1em',fontFamily:'monospace',fontSize:'1.1em',fontWeight:600}}>{c.candidat_numero}</td>
                        <td style={{padding:'1em'}}>
                          <input 
                            type="number" 
                            min="0" max="20" step="0.25"
                            value={c.noteInput}
                            onChange={(e) => handleNoteChange(c.dossier_id, e.target.value)}
                            disabled={c.note?.etat === 'valide' && user.role !== 'president_jury'}
                            style={{padding:'0.5em',width:80,borderRadius:6,border:'1px solid #ddd'}}
                          />
                        </td>
                        <td style={{padding:'1em'}}>
                          {c.note ? (
                            <span style={{
                              padding:'0.3em 0.8em',borderRadius:20,fontSize:'0.85em',
                              background: c.note.etat === 'valide' ? '#d1fae5' : '#fff7ed',
                              color: c.note.etat === 'valide' ? '#065f46' : '#9a3412'
                            }}>
                              {c.note.etat === 'valide' ? 'Validé' : 'Brouillon'}
                            </span>
                          ) : <span style={{color:'#999'}}>Non noté</span>}
                        </td>
                        <td style={{padding:'1em'}}>
                          {/* Correcteur actions */}
                          {user.role === 'correcteur' && c.note?.etat !== 'valide' && (
                            <button 
                              onClick={() => saveNote(c)}
                              disabled={saving[c.dossier_id]}
                              style={{padding:'0.5em 1em',background:'#0d6efd',color:'#fff',border:'none',borderRadius:6,cursor:'pointer'}}
                            >
                              {saving[c.dossier_id] ? '...' : 'Enregistrer'}
                            </button>
                          )}
                          
                          {/* President actions */}
                          {user.role === 'president_jury' && (
                            <div style={{display:'flex',gap:'0.5em'}}>
                              <button 
                                onClick={() => saveNote(c)}
                                disabled={saving[c.dossier_id]}
                                style={{padding:'0.5em 1em',background:'#0d6efd',color:'#fff',border:'none',borderRadius:6,cursor:'pointer'}}
                              >
                                {saving[c.dossier_id] ? '...' : 'Enregistrer'}
                              </button>
                              {c.note && c.note.etat !== 'valide' && (
                                <button 
                                  onClick={() => validerNote(c.note.id)}
                                  style={{padding:'0.5em 1em',background:'#059669',color:'#fff',border:'none',borderRadius:6,cursor:'pointer'}}
                                >
                                  Valider
                                </button>
                              )}
                            </div>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )
            )}
          </div>
        )}

        {/* Deliberation View */}
        {activeTab === 'deliberation' && selectedSerie && (
          <div style={{background:'#fff',padding:'1.5em',borderRadius:12,boxShadow:'0 2px 8px #0001'}}>
            <div style={{fontSize:18,fontWeight:700,marginBottom:'1em'}}>Classement Provisoire (Anonyme)</div>
            {loading ? <div>Calcul du classement...</div> : (
              !classement || classement.length === 0 ? <div>Aucun résultat disponible pour cette série.</div> : (
                <table style={{width:'100%',borderCollapse:'collapse'}}>
                  <thead>
                    <tr style={{textAlign:'left',borderBottom:'2px solid #eee'}}>
                      <th style={{padding:'1em'}}>Rang</th>
                      <th style={{padding:'1em'}}>Anonymat</th>
                      <th style={{padding:'1em'}}>Moyenne</th>
                    </tr>
                  </thead>
                  <tbody>
                    {classement.map((row, index) => (
                      <tr key={row.numero_candidat} style={{borderBottom:'1px solid #eee'}}>
                        <td style={{padding:'1em',fontWeight:700}}>#{index + 1}</td>
                        <td style={{padding:'1em',fontFamily:'monospace',fontSize:'1.1em'}}>{row.numero_candidat}</td>
                        <td style={{padding:'1em',fontWeight:700,color:'#0d6efd'}}>{row.moyenne} / 20</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )
            )}
          </div>
        )}

      </div>
    </div>
  );
}
