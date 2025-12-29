import React from 'react';
import LoginRoleTemplate from './LoginRoleTemplate';

export default function LoginJuryPage() {
  return <LoginRoleTemplate expectedRole="jury" title="Connexion Jury" redirect="/jury" />;
}