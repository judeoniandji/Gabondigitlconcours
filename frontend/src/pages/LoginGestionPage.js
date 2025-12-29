import React from 'react';
import LoginRoleTemplate from './LoginRoleTemplate';

export default function LoginGestionPage() {
  return <LoginRoleTemplate expectedRole="gestionnaire" title="Connexion Gestion" redirect="/dashboard" />;
}