import React from 'react';
import LoginRoleTemplate from './LoginRoleTemplate';

export default function LoginCandidatePage() {
  return <LoginRoleTemplate expectedRole="candidat" title="Connexion Candidat" redirect="/candidat" />;
}