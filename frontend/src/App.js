import React, {Component} from 'react';
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import LandingPage from './components/LandingPage/LandingPage';
import TestPage from './TestPage';
import OauthHelper from './components/OauthHelper';
import Particles from "react-particles-js";
import 'bootstrap/dist/css/bootstrap.min.css';

const particlesOptions = {
  particles: {
    number: {
      value: 80,
      density: {
        enable: true,
        value_area: 800
      }
    }
  }
};

export default class App extends Component {
  render(){
    return (
      <div>
        <Router>
          <Particles className="particles" params={particlesOptions} /> 
          <Switch>
            <Route exact path = "/" component = {LandingPage}/>
            <Route path = "/test" component = {TestPage} />
            <Route path = "/oauth-complete" component={OauthHelper}/>
          </Switch>
        </Router>
      </div>
    );      
  }
}