import React, { useEffect, useState } from 'react';
import { useAuth0, withAuthenticationRequired } from '@auth0/auth0-react';

function Tests() {
  const { getAccessTokenSilently, getAccessTokenWithPopup } = useAuth0();
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);
  const [refreshIndex, setRefreshIndex] = useState(0);
  const [value, setValue] = useState("");
  const getOpts = {
        audience: 'https://medical-measurement',
        scope: 'get:tests',
      };
  const getTokenAndTryAgain = async () => {
    await getAccessTokenWithPopup(getOpts);
    setRefreshIndex(refreshIndex + 1);
  };

  useEffect(() => {
      getAccessTokenSilently(getOpts)
      .then(token => fetch("/tests", {
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
  }, [refreshIndex])

  const handleChange = (evt) => {
      setValue(evt.target.value);
  }

  const handleSubmit = (evt) => {
      getAccessTokenSilently({
        audience: 'https://medical-measurement',
        scope: 'post:tests',
      })
      .then(token => fetch("/tests", {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({name: value})
        }))
      .then(res => res.json())
      .then(
        (result) => {
          if(result.success){
            alert(`Creating new test ${value}`);
          }
          else{
            alert(`Error (#` + result.error + '): ' + result.message);
          }
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
        {items.map(item => (
          <li key={item.id}>
            Test ID {item.id}: {item.name}
          </li>
        ))}
      <form onSubmit={handleSubmit}>
        <label>
          Name:
          <input type="text" value={value.value} onChange={handleChange} /></label>
        <input type="submit" value="Submit" />
      </form>
      </ul>
    );
  }
}

export default Tests;