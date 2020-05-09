import React, {Component} from 'react';
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import LandingPage from './components/LandingPage/LandingPage';
import OauthHelper from './components/OauthHelper';
import Particles from "react-particles-js";
import Dashboard from "./components/Dashboard/DashboardMain"
import 'bootstrap/dist/css/bootstrap.min.css';
import DashActive from './components/Dashboard/DashActive';
import DashNew from './components/Dashboard/DashNew';
import {particlesOptions} from './particlesOptions';

export default class App extends Component {
  render(){
    return (
      <div>
        <Router>
          <Particles className="particles" params={particlesOptions} /> 
          <Switch>
            <Route exact path = "/" component = {LandingPage}/>
            <Route path = "/oauth-complete" component={OauthHelper}/>
            <Route exact path = "/dashboard" component = {Dashboard} />
            <Route path = "/dashboard/active" component={DashActive}/>
            <Route path = "/dashboard/new" component={DashNew}/>
          </Switch>
        </Router>
      </div>
    );      
  }
}