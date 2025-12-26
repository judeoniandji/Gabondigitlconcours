import AirtelMoneyLogo from './airtel-money-logo.png';

export default function AirtelMoneyButton({ onClick, disabled }) {
  return (
    <button onClick={onClick} disabled={disabled} style={{background:'#d80027',color:'#fff',padding:'0.7em 1.2em',border:'none',borderRadius:'4px',display:'flex',alignItems:'center',gap:'0.5em',fontWeight:'bold',fontSize:'1rem',cursor:'pointer'}}>
      <img src={AirtelMoneyLogo} alt="Airtel Money" style={{height:'24px'}} />
      Payer avec Airtel Money
    </button>
  );
}
