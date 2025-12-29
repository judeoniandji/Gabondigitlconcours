import React from 'react';
import LoginRoleTemplate from './LoginRoleTemplate';

export default function LoginSecretairePage() {
  return <LoginRoleTemplate expectedRole="secretaire" title="Connexion Secrétaire" redirect="/secretaire" />;
}