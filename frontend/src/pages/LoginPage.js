import React, { useState, useEffect } from 'react';
import api from '../services/api';

export default function LoginPage() {
  const [concours, setConcours] = useState([]);

  useEffect(() => {
    api.get('concours/concours/?ouvert=true').then(res => {
      setConcours(res.data || []);
    }).catch(() => {});
  }, []);

  return (
    <div style={{minHeight:'100vh',display:'flex',alignItems:'center',justifyContent:'center',background:'linear-gradient(135deg,#0d6efd 0%,#00b894 100%)'}}>
      <div style={{width:'100%',maxWidth:480,background:'#fff',borderRadius:16,boxShadow:'0 16px 40px #0002',overflow:'hidden'}}>
        <div style={{padding:'1.25em 1.5em',background:'#f7f9fc',display:'flex',alignItems:'center',gap:'0.75em',justifyContent:'space-between'}}>
          <div style={{display:'flex',alignItems:'center',gap:'0.75em'}}>
            <div style={{width:36,height:36,borderRadius:8,background:'#0d6efd'}} />
            <div style={{fontWeight:800,fontSize:18}}>République Gabonaise</div>
          </div>
          <div style={{color:'#667085',fontSize:13}}>Plateforme officielle des concours administratifs</div>
        </div>
        <div style={{padding:'1.75em 1.5em'}}>
          <div style={{marginBottom:'1.5em'}}>
            <div style={{fontSize:26,fontWeight:800}}>Plateforme des Concours Administratifs</div>
            <div style={{color:'#666'}}>République Gabonaise</div>
          </div>
          
          <div style={{marginBottom:'2em'}}>
            {concours.length > 0 ? (
              <>
                <div style={{fontWeight:800,marginBottom:'0.75em',fontSize:20,color:'#0d6efd'}}>🎓 Concours ouverts aux inscriptions</div>
                <div style={{display:'grid',gap:'0.75em',maxHeight:320,overflowY:'auto',marginBottom:'1em'}}>
                  {concours.map(c => (
                    <div key={c.id} style={{border:'1px solid #e4e7ec',borderRadius:10,padding:'1em',background:'#f7f9fc'}}>
                      <div style={{fontWeight:700,color:'#0d6efd',marginBottom:'0.4em',fontSize:16}}>{c.nom}</div>
                      {c.ministere_organisateur && (
                        <div style={{fontSize:12,color:'#667085',marginBottom:'0.3em',fontWeight:600}}>
                          🏛️ {c.ministere_organisateur}
                        </div>
                      )}
                      {c.description && (
                        <div style={{fontSize:12,color:'#667085',marginBottom:'0.5em'}}>
                          {c.description.substring(0, 120)}{c.description.length > 120 ? '...' : ''}
                        </div>
                      )}
                      <div style={{display:'grid',gap:'0.3em',marginBottom:'0.5em'}}>
                        {c.niveau_demande && (
                          <div style={{fontSize:12,color:'#555'}}>
                            📚 Niveau: <span style={{fontWeight:600}}>{c.niveau_demande}</span>
                          </div>
                        )}
                        {c.limite_age_display && (
                          <div style={{fontSize:12,color:'#555'}}>
                            👤 Âge: <span style={{fontWeight:600}}>{c.limite_age_display}</span>
                          </div>
                        )}
                        {c.nombre_places && (
                          <div style={{fontSize:12,color:'#555'}}>
                            🎯 Places: <span style={{fontWeight:600}}>{c.nombre_places}</span>
                          </div>
                        )}
                      </div>
                      <div style={{display:'grid',gap:'0.3em',marginTop:'0.5em',paddingTop:'0.5em',borderTop:'1px solid #e4e7ec'}}>
                        <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}>
                          <div style={{fontSize:12,color:'#667085'}}>
                            📅 {new Date(c.date_ouverture).toLocaleDateString('fr-FR')} - {new Date(c.date_fermeture).toLocaleDateString('fr-FR')}
                          </div>
                        </div>
                        <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}>
                          <div style={{fontSize:12,color:'#667085'}}>
                            💰 Frais d'inscription:
                          </div>
                          <div style={{fontWeight:700,color:'#28a745',fontSize:14}}>{c.frais_inscription} FCFA</div>
                        </div>
                      </div>
                      {c.lieu_depot && (
                        <div style={{fontSize:11,color:'#888',marginTop:'0.4em',fontStyle:'italic'}}>
                          📍 {c.lieu_depot.substring(0, 80)}{c.lieu_depot.length > 80 ? '...' : ''}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </>
            ) : (
              <div style={{padding:'1em',background:'#f7f9fc',borderRadius:10,border:'1px solid #e4e7ec',marginBottom:'1em',textAlign:'center',color:'#667085'}}>
                Aucun concours ouvert pour le moment
              </div>
            )}
            <a href="/register" style={{display:'block',padding:'1em',background:'#28a745',color:'#fff',border:'none',borderRadius:10,fontWeight:700,textAlign:'center',textDecoration:'none',marginTop:'0.5em'}}>
              🎓 Je suis étudiant - Créer un compte
            </a>
          </div>

          <div style={{borderTop:'1px solid #f0f2f5',paddingTop:'1.5em'}}>
            <div style={{fontWeight:800,marginBottom:'0.75em',fontSize:18}}>Connexion pour les membres</div>
            <div style={{fontSize:13,color:'#667085',marginBottom:'1em'}}>Vous êtes membre du jury, secrétaire, gestionnaire ?</div>
            <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(140px,1fr))',gap:'0.75em'}}>
              <a href="/login/jury" style={{display:'block',padding:'0.9em',border:'1px solid #e4e7ec',borderRadius:12,textDecoration:'none',color:'#0d6efd',fontWeight:700,textAlign:'center',background:'#f7f9fc',transition:'all 150ms ease'}} aria-label="Connexion Jury">🧑‍⚖️ Jury</a>
              <a href="/login/correcteur" style={{display:'block',padding:'0.9em',border:'1px solid #e4e7ec',borderRadius:12,textDecoration:'none',color:'#0d6efd',fontWeight:700,textAlign:'center',background:'#f7f9fc',transition:'all 150ms ease'}} aria-label="Connexion Correcteur">📝 Correcteur</a>
              <a href="/login/secretaire" style={{display:'block',padding:'0.9em',border:'1px solid #e4e7ec',borderRadius:12,textDecoration:'none',color:'#0d6efd',fontWeight:700,textAlign:'center',background:'#f7f9fc',transition:'all 150ms ease'}} aria-label="Connexion Secrétariat">🗂️ Secrétariat</a>
              <a href="/login/gestion" style={{display:'block',padding:'0.9em',border:'1px solid #e4e7ec',borderRadius:12,textDecoration:'none',color:'#0d6efd',fontWeight:700,textAlign:'center',background:'#f7f9fc',transition:'all 150ms ease'}} aria-label="Connexion Gestion">⚙️ Gestion</a>
              <a href="/login/president" style={{display:'block',padding:'0.9em',border:'1px solid #e4e7ec',borderRadius:12,textDecoration:'none',color:'#0d6efd',fontWeight:700,textAlign:'center',background:'#f7f9fc',transition:'all 150ms ease'}} aria-label="Connexion Président">👔 Président</a>
            </div>
            <div style={{marginTop:'0.75em',color:'#667085',fontSize:13}}>Vos données sont protégées</div>
          </div>
          <div style={{marginTop:'1.5em',borderTop:'1px solid #f0f2f5',paddingTop:'0.75em',color:'#667085',fontSize:12,textAlign:'center'}}>
            Plateforme officielle des concours administratifs · République Gabonaise<br />© 2025 – Accès sécurisé
          </div>
        </div>
      </div>
    </div>
  );
}
