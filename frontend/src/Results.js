import React, { useEffect, useState } from 'react';
import { useAuth0, withAuth0 } from '@auth0/auth0-react';

class Result extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      items: []
    };
  }

  componentDidMount() {
    const {getAccessTokenSilently} = this.props.auth0;
    const token = getAccessTokenSilently();
    fetch("/results", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
    .then(res => res.json())
    .then(
      (result) => {
        this.setState({
          isLoaded: true,
          items: result.message.data
        });
      },
      // Note: it's important to handle errors here
      // instead of a catch() block so that we don't swallow
      // exceptions from actual bugs in components.
      (error) => {
        this.setState({
          isLoaded: true,
          error
        });
      }
    )
  }

  render() {
    const { error, isLoaded, items } = this.state;
    if (error) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else {
      return (
        <ul>
          {items.map(item => (
            <li key={item.id}>
              ID: {item.test_id} at {item.time}: {item.value}
            </li>
          ))}
        </ul>
      );
    }
  }
}

export default withAuth0(Result);