import React from 'react';
import LoginRoleTemplate from './LoginRoleTemplate';

export default function LoginPresidentPage() {
  return <LoginRoleTemplate expectedRole="president_jury" title="Connexion Président de jury" redirect="/jury" />;
}