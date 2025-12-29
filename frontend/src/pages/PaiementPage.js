import React, { useState } from 'react';
import AirtelMoneyButton from '../components/AirtelMoneyButton';
import api from '../services/api';

export default function PaiementPage() {
  const [montant, setMontant] = useState('');
  const [reference, setReference] = useState('');
  const [msisdn, setMsisdn] = useState('');
  const [status, setStatus] = useState('');
  const displayMontant = montant ? `${montant} FCFA` : '';
  const [msisdnError, setMsisdnError] = useState('');

  const validateMsisdnGabon = (value) => {
    if (!value) return '';
    const v = String(value).replace(/\s+/g, '');
    if (v.startsWith('+')) {
      return /^\+241\d{8}$/.test(v) ? '' : 'Format attendu: +241 suivi de 8 chiffres';
    }
    return /^\d{8}$/.test(v) ? '' : 'Format attendu: 8 chiffres (ex: 06234567)';
  };

  const handlePaiement = async () => {
    setStatus('Paiement en cours...');
    const err = validateMsisdnGabon(msisdn);
    setMsisdnError(err);
    if (err) { setStatus('Numéro Airtel invalide'); return; }
    try {
      const res = await api.post('payments/paiements/airtel/', {
        msisdn,
        amount: montant,
        reference,
        concours_id: 1,
        candidat_id: 1,
      });
      setStatus(`Paiement initié. Réponse: ${JSON.stringify(res.data)}`);
    } catch (e) {
      setStatus('Erreur paiement');
    }
  };

  return (
    <div style={{maxWidth:420,margin:'auto',padding:'2em'}}>
      <h2>Paiement Airtel Money</h2>
      <input type="text" placeholder="Montant (FCFA)" value={montant} onChange={e=>setMontant(e.target.value)} style={{width:'100%',padding:'0.5em',marginBottom:'0.5em'}} />
      {displayMontant && <div style={{marginBottom:'0.8em',color:'#555'}}>Montant: {displayMontant}</div>}
      <input type="text" placeholder="Référence" value={reference} onChange={e=>setReference(e.target.value)} style={{width:'100%',padding:'0.5em',marginBottom:'1em'}} />
      <input type="text" placeholder="Numéro Airtel (ex: 06234567 ou +24162345678)" value={msisdn} onChange={e=>{ setMsisdn(e.target.value); setMsisdnError(validateMsisdnGabon(e.target.value)); }} style={{width:'100%',padding:'0.5em',marginBottom:'0.25em'}} />
      {msisdnError ? <div style={{color:'#b00020',marginBottom:'0.75em'}}>{msisdnError}</div> : <div style={{color:'#667085',marginBottom:'0.75em',fontSize:12}}>Format Gabon: 8 chiffres ou +241 suivi de 8 chiffres</div>}
      <div style={{display:'flex',alignItems:'center',gap:'0.75em'}}>
        <AirtelMoneyButton onClick={handlePaiement} disabled={!montant || !reference || !msisdn || !!msisdnError} />
        {displayMontant && <div style={{fontWeight:'bold'}}>{displayMontant}</div>}
      </div>
      {status && <div style={{marginTop:'1em'}}>{status}</div>}
    </div>
  );
}
