import React from "react";
import ReactDOM from "react-dom";
import Main from "./Main";
import "./index.css";
import { Auth0Provider } from "@auth0/auth0-react";

ReactDOM.render(
  <Auth0Provider
    domain="balazsszalai.auth0.com"
    clientId="Ijleo40NJaKF4t0IUPCfXovwzUgyzGnj"
    redirectUri="http://127.0.0.1:3000/#/"
  >
    <Main />
  </Auth0Provider>,
  document.getElementById("root")
);