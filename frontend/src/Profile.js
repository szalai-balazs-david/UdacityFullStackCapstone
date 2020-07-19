import React, { useEffect, useState } from 'react';
import { useAuth0 } from '@auth0/auth0-react';

const Profile = () => {
  const { getAccessTokenSilently } = useAuth0();
  const [user, setUser] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        const token = await getAccessTokenSilently({
          audience: 'https://medical-measurement',
          scope: 'get:doctors',
        });
        const response = await fetch('/user', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setUser(await response.json());
      } catch (e) {
        console.error(e);
      }
    })();
  }, [getAccessTokenSilently]);

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <ul>
      <p>User information:</p>
      <p>User ID: {user.message.id}</p>
      <p>Name: {user.message.name}</p>
      {user.message.tests.length > 0
        ? <p>Tests on file:</p>
        : <p>No tests on file</p>}
      {user.message.tests.length > 0 && user.message.tests.map((test, index) => {
        return <li key={index}>{test.name} (Test ID: {test.id})</li>
      })}
    </ul>
  );
};

export default Profile;