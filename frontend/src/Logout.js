import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';

function LogoutButton() {
  const {
    isAuthenticated,
    logout,
  } = useAuth0();

  return isAuthenticated && (
    <button onClick={() => {
      logout({ returnTo: "http://127.0.0.1:3000/#/" });
    }}>Log out</button>
  );
}

export default LogoutButton;