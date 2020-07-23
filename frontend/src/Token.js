import React, { useEffect, useState } from 'react';
import { useAuth0, withAuthenticationRequired } from '@auth0/auth0-react';

const Token = () => {
  const { getAccessTokenSilently, getAccessTokenWithPopup } = useAuth0();
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [token, setToken] = useState("");
  const [refreshIndex, setRefreshIndex] = useState(0);
  const getOpts = {
        audience: 'https://medical-measurement',
        scope: 'get:profile',
      };
  const getTokenAndTryAgain = async () => {
    await getAccessTokenWithPopup(getOpts);
    setRefreshIndex(refreshIndex + 1);
  };

  useEffect(() => {
      getAccessTokenSilently(getOpts)
      .then(token =>
        {setToken(token);
        setIsLoaded(true);},
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          setError(error);
          setIsLoaded(true);
        }
      )
  }, [refreshIndex])

  if (error) {
    if (error.error === 'consent_required') {
      return (
        <button onClick={getTokenAndTryAgain}>Consent to reading users</button>
      );
    }
    return <div>Error: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>Loading...</div>;
  } else {
  return (
    <ul>
      <p>Token: {token}</p>
    </ul>
  );}
};

export default withAuthenticationRequired(Token);