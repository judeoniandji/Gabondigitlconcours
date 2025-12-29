import React from 'react';
import LoginRoleTemplate from './LoginRoleTemplate';

export default function LoginCorrecteurPage() {
  return <LoginRoleTemplate expectedRole="correcteur" title="Connexion Correcteur" redirect="/jury" />;
}