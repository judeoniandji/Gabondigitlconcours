import React, { useState } from 'react';
import AirtelMoneyButton from '../components/AirtelMoneyButton';

export default function PaiementPage() {
  const [montant, setMontant] = useState('');
  const [reference, setReference] = useState('');
  const [msisdn, setMsisdn] = useState('');
  const [status, setStatus] = useState('');

  const handlePaiement = async () => {
    setStatus('Paiement en cours...');
    // TODO: Appeler l'API backend pour initier le paiement Airtel Money
    setTimeout(() => setStatus('Paiement simulé (sandbox)'), 2000);
  };

  return (
    <div style={{maxWidth:400,margin:'auto',padding:'2em'}}>
      <h2>Paiement Airtel Money</h2>
      <input type="text" placeholder="Montant" value={montant} onChange={e=>setMontant(e.target.value)} style={{width:'100%',padding:'0.5em',marginBottom:'1em'}} />
      <input type="text" placeholder="Référence" value={reference} onChange={e=>setReference(e.target.value)} style={{width:'100%',padding:'0.5em',marginBottom:'1em'}} />
      <input type="text" placeholder="Numéro Airtel (msisdn)" value={msisdn} onChange={e=>setMsisdn(e.target.value)} style={{width:'100%',padding:'0.5em',marginBottom:'1em'}} />
      <AirtelMoneyButton onClick={handlePaiement} disabled={!montant || !reference || !msisdn} />
      {status && <div style={{marginTop:'1em'}}>{status}</div>}
    </div>
  );
}
