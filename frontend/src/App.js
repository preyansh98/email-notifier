import React, {Component} from 'react';
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import LandingPage from './components/LandingPage/LandingPage';
import TestPage from './TestPage';

export default class App extends Component {
  render(){
    return (
      <div>
      <Router>
        <Switch>
          <Route exact path="/" component={LandingPage}/>
          <Route path="/test" component={TestPage}/>
        </Switch>
      </Router>
      </div>
    );
  }
}