import React, { useEffect, useState } from 'react';
import { useAuth0, withAuth0 } from '@auth0/auth0-react';
import { useApi } from './use-api';

const Profile = () => {
  const opts = {
    audience: 'https://medical-measurement',
    scope: 'get:doctors',
  };
  const { login, getAccessTokenWithPopup } = useAuth0();
  const { loading, error, refresh, data: users } = useApi(
    'http://127.0.0.1:5000/tests',
    opts
  );
  const getTokenAndTryAgain = async () => {
    await getAccessTokenWithPopup(opts);
    refresh();
  };
  if (loading) {
    return <div>Loading...</div>;
  }
  if (error) {
    if (error.error === 'login_required') {
      return <button onClick={() => login(opts)}>Login</button>;
    }
    if (error.error === 'consent_required') {
      return (
        <button onClick={getTokenAndTryAgain}>Consent to reading users</button>
      );
    }
    return <div>Oops {error.message}</div>;
  }
  return (
    <ul>
      {users}
    </ul>
  );
};

export default Profile;