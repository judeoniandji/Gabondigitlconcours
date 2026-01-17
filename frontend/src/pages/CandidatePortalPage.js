import React, { useEffect, useState } from 'react';
import api from '../services/api';

export default function CandidatePortalPage() {
  const [userId, setUserId] = useState(null);
  const [candidatId, setCandidatId] = useState(null);
  const [concours, setConcours] = useState([]);
  const [series, setSeries] = useState([]);
  const [dossiers, setDossiers] = useState([]);
  
  const [selectedConcours, setSelectedConcours] = useState('');
  const [selectedSerie, setSelectedSerie] = useState('');
  const [availableSeries, setAvailableSeries] = useState([]);
  
  const [status, setStatus] = useState('');

  useEffect(() => {
    const access = localStorage.getItem('access');
    if (!access) { window.location.href = '/'; return; }
    try {
      const payload = JSON.parse(atob(access.split('.')[1]));
      setUserId(payload.user_id);
    } catch {
      api.get('users/me/').then(res => {
        if (res && res.data && res.data.id) setUserId(res.data.id);
      }).catch(() => {});
    }
  }, []);

  useEffect(() => {
    const load = async () => {
      const resC = await api.get('concours/concours/?ouvert=true');
      setConcours(resC.data);
      const resS = await api.get('concours/series/');
      setSeries(resS.data);
      
      const resCand = await api.get('users/candidats/');
      const me = resCand.data.find(c => c.user && c.user.id === userId);
      if (me) {
        setCandidatId(me.id);
        const resD = await api.get(`concours/dossiers/?candidat_id=${me.id}`);
        setDossiers(resD.data);
      }
    };
    if (userId) load();
  }, [userId]);

  // Update available series when concours changes
  useEffect(() => {
    if (selectedConcours) {
      const filtered = series.filter(s => s.concours === Number(selectedConcours));
      setAvailableSeries(filtered);
      setSelectedSerie('');
    } else {
      setAvailableSeries([]);
    }
  }, [selectedConcours, series]);

  const apply = async () => {
    if (!candidatId || !selectedConcours) return;
    if (availableSeries.length > 0 && !selectedSerie) {
      setStatus('Veuillez sélectionner une série');
      return;
    }
    
    setStatus('Soumission en cours...');
    const reference = `REF-${Date.now()}-${Math.floor(Math.random()*10000)}`;
    try {
      const payload = { 
        candidat: candidatId, 
        concours: selectedConcours, 
        reference 
      };
      if (selectedSerie) {
        payload.serie = selectedSerie;
      }
      
      await api.post('concours/dossiers/', payload);
      const resD = await api.get(`concours/dossiers/?candidat_id=${candidatId}`);
      setDossiers(resD.data);
      setStatus('Dossier soumis');
      setSelectedConcours('');
      setSelectedSerie('');
    } catch (e) {
      setStatus('Erreur de soumission: ' + (e.response?.data?.detail || e.message));
    }
  };

  return (
    <div style={{minHeight:'100vh',background:'#f5f7fb',padding:'2em'}}>
      <div style={{maxWidth:980,margin:'0 auto'}}>
        <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}>
          <div>
            <div style={{fontSize:24,fontWeight:800}}>Espace Candidat</div>
            <div style={{color:'#667085'}}>Vos données sont protégées</div>
          </div>
          <button onClick={() => { localStorage.removeItem('access'); window.location.href = '/login/candidat'; }} style={{background:'#fff',border:'1px solid #ddd',padding:'0.5em 1em',borderRadius:6}}>Déconnexion</button>
        </div>
        
        <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:'1em',marginTop:'1em'}}>
          <div style={{background:'#fff',borderRadius:12,boxShadow:'0 8px 24px #0001',padding:'1em'}}>
            <div style={{fontWeight:700,marginBottom:'0.5em'}}>Postuler à un concours</div>
            <div style={{display:'grid',gap:'0.75em'}}>
              <select value={selectedConcours} onChange={e=>setSelectedConcours(e.target.value)} style={{width:'100%',padding:'0.7em',border:'1px solid #e4e7ec',borderRadius:10}}>
                <option value="">Sélectionner un concours...</option>
                {concours.map(c => (<option key={c.id} value={c.id}>{c.nom} — {c.frais_inscription} FCFA</option>))}
              </select>
              
              {availableSeries.length > 0 && (
                <select value={selectedSerie} onChange={e=>setSelectedSerie(e.target.value)} style={{width:'100%',padding:'0.7em',border:'1px solid #e4e7ec',borderRadius:10}}>
                  <option value="">Sélectionner une série...</option>
                  {availableSeries.map(s => (<option key={s.id} value={s.id}>{s.nom}</option>))}
                </select>
              )}
              
              <button onClick={apply} style={{padding:'0.8em 1.2em',background:'#0d6efd',color:'#fff',border:'none',borderRadius:10,fontWeight:700}}>Soumettre ma candidature</button>
            </div>
            {status && <div style={{marginTop:'0.75em',color: status.includes('Erreur') ? 'red' : '#0d6efd'}}>{status}</div>}
          </div>
          
          <div style={{background:'#fff',borderRadius:12,boxShadow:'0 8px 24px #0001',padding:'1em'}}>
            <div style={{fontWeight:700,marginBottom:'0.5em'}}>Mes dossiers</div>
            <div style={{display:'grid',gap:'0.5em'}}>
              {dossiers.map(d => {
                const c = concours.find(x => x.id === d.concours);
                const s = series.find(x => x.id === d.serie);
                return (
                  <div key={d.id} style={{border:'1px solid #e4e7ec',borderRadius:10,padding:'0.7em'}}>
                    <div style={{fontWeight:600}}>{c ? c.nom : `Concours #${d.concours}`}</div>
                    {s && <div style={{fontSize:'0.9em',color:'#555'}}>Série: {s.nom}</div>}
                    <div style={{marginTop:5}}>Statut: <span style={{fontWeight:600}}>{d.statut}</span></div>
                    <div style={{fontSize:'0.8em',color:'#888'}}>Réf: {d.reference || '—'}</div>
                  </div>
                );
              })}
              {dossiers.length === 0 && <div style={{color:'#667085'}}>Aucun dossier pour le moment</div>}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
