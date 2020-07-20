import React, { Component } from "react";
import {
  Route,
  NavLink,
  HashRouter
} from "react-router-dom";
import Home from "./Home";
import Profile from "./Profile";
import Result from "./Results";
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
                        <li><NavLink to="/results">Results</NavLink></li>
                    </ul>
                    <div className="content">
                        <Route exact path="/" component={Home}/>
                        <Route path="/profile" component={Profile}/>
                        <Route path="/results" component={Result}/>
                    </div>
                </div>
            </HashRouter>
        );
    }
}

export default Main;