import React, { useEffect, useState } from 'react';
import { useAuth0 } from '@auth0/auth0-react';

function Result() {
  const { getAccessTokenSilently } = useAuth0();
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);

  useEffect(() => {
      getAccessTokenSilently({
        audience: 'https://medical-measurement',
        scope: 'get:doctors',
      })
      .then(token => fetch("/results", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }))
      .then(res => res.json())
      .then(
        (result) => {
          setItems(result.message);
          setIsLoaded(true);
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      )
  }, [])

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>Loading...</div>;
  } else {
    return (
      <ul>
        {items.data.map(item => (
          <li key={item.id}>
            ID: {item.test_id} at {item.time}: {item.value}
          </li>
        ))}
      </ul>
    );
  }
}

export default Result;