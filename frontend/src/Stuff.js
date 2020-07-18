import React, { useEffect, useState } from 'react';
import { useAuth0, withAuth0 } from '@auth0/auth0-react';

const Stuff = () => {
  const { getAccessTokenSilently, getTokenWithPopup } = useAuth0();
  const [posts, setPosts] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        const token = await getAccessTokenSilently({
          audience: 'https://medical-measurement',
          scope: 'get:doctors',
        });
        const response = await fetch('http://127.0.0.1:5000/tests', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setPosts(await response.json());
      } catch (e) {
        console.error(e);
      }
    })();
  }, [getAccessTokenSilently]);

  if (!posts) {
    return <div>Loading...</div>;
  }

  return (
    <ul>
      {posts.map((post, index) => {
        return <li key={index}>{post}</li>;
      })}
    </ul>
  );
};

export default Stuff;