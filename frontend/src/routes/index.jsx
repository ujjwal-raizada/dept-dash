import React, { Component } from "react";
import { Route, Switch } from "react-router-dom";
import { Redirect } from "react-router";

import { loadProgressBar } from "axios-progress-bar";
import "../assets/progress-bar.css";

import { Home, ErrorPage404 } from "./LazyLoadRoutes";

loadProgressBar();

export default class Routes extends Component {
  constructor(props) {
    super(props);
    this.state = { token: null };
  }
  setToken(token) {
    this.setState({ token });
  }
  render() {
    return (
      <main>
        <Switch className="main">
          <Route exact path="/" component={Home} />
          <Route component={ErrorPage404} />
        </Switch>
      </main>
    )
  }
}
