import React, { useEffect, useState } from 'react';
import { useAuth0, withAuthenticationRequired } from '@auth0/auth0-react';

function Result() {
  const { getAccessTokenSilently } = useAuth0();
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);
  const [value, setValue] = useState(0);

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

  const handleChange = (evt) => {
      setValue(evt.target.value);
  }

  const handleSubmit = (evt) => {
      getAccessTokenSilently({
        audience: 'https://medical-measurement',
        scope: 'get:doctors',
      })
      .then(token => fetch("/results", {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({test_id: 1, time: new Date().toLocaleString(), value: value})
        }))
      .then(res => res.json())
      .then(
        (result) => {
          alert(`Submitting Result ${value}`);
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          alert('Error: ' + error);
        }
      )
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>Loading...</div>;
  } else {
    return (
      <ul>
        {items.data.map(item => (
          <li key={item.id}>
            Test ID: {item.test_id} at {item.time}: {item.value}
          </li>
        ))}
      <form onSubmit={handleSubmit}>
        <label>
          Value:
          <input type="number" value={value.value} onChange={handleChange} /></label>
        <input type="submit" value="Submit" />
      </form>
      </ul>
    );
  }
}

export default withAuthenticationRequired(Result);