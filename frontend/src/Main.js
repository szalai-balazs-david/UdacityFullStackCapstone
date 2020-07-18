import React, { Component } from "react";
import {
  Route,
  NavLink,
  HashRouter
} from "react-router-dom";
import Home from "./Home";
import Stuff from "./Stuff";
import Contact from "./Contact";
import LoginButton from "./Login";
import LogoutButton from "./Logout";
import Profile from "./Profile";
import App from "./App";

class Main extends Component {
    render() {
        return (
            <HashRouter>
                <h1>Medical Test Result Collector</h1>
                <App />
                <div>
                    <ul className="header">
                        <li><NavLink exact to="/">Home</NavLink></li>
                        <li><NavLink to="/stuff">Stuff</NavLink></li>
                        <li><NavLink to="/contact">Contact</NavLink></li>
                        <li><NavLink to="/profile">Profile</NavLink></li>
                        <li><NavLink to="/login">Login</NavLink></li>
                        <li><NavLink to="/logout">Logout</NavLink></li>
                    </ul>
                    <div className="content">
                        <Route exact path="/" component={Home}/>
                        <Route path="/stuff" component={Stuff}/>
                        <Route path="/contact" component={Contact}/>
                        <Route path="/profile" component={Profile}/>
                        <Route path="/login" component={LoginButton}/>
                        <Route path="/logout" component={LogoutButton}/>
                    </div>
                </div>
            </HashRouter>
        );
    }
}

export default Main;