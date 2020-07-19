import React, { Component } from "react";
import {
  Route,
  NavLink,
  HashRouter
} from "react-router-dom";
import Home from "./Home";
import Stuff from "./Stuff";
import Profile from "./Profile";
import Contact from "./Contact";
import Authentication from "./Authentication";

class Main extends Component {
    render() {
        return (
            <HashRouter>
                <h1>Medical Test Result Collector</h1>
                <Authentication />
                <div>
                    <ul className="header">
                        <li><NavLink exact to="/">Home</NavLink></li>
                        <li><NavLink to="/profile">Profile</NavLink></li>
                    </ul>
                    <div className="content">
                        <Route exact path="/" component={Home}/>
                        <Route path="/Profile" component={Profile}/>
                    </div>
                </div>
            </HashRouter>
        );
    }
}

export default Main;