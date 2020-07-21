import React, { useEffect, useState } from 'react';
import { useAuth0, withAuthenticationRequired } from '@auth0/auth0-react';

const Profile = () => {
  const { getAccessTokenSilently, getAccessTokenWithPopup } = useAuth0();
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);
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
      .then(token => fetch("/profile", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }))
      .then(res => res.json())
      .then(
        (result) => {
          if(result.success){
            setItems(result.message);
            setIsLoaded(true);
          }
          else{
            alert(`Error (#` + result.error + '): ' + result.message);
          }
        },
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
      <p>User information:</p>
      <p>User ID: {items.id}</p>
      <p>Name: {items.name}</p>
      {items.tests.length > 0
        ? <p>Tests on file:</p>
        : <p>No tests on file</p>}
      {items.tests.length > 0 && items.tests.map((test, index) => {
        return <li key={index}>{test.name} (Test ID: {test.id})</li>
      })}
    </ul>
  );}
};

export default withAuthenticationRequired(Profile);