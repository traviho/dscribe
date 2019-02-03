import React, { Component } from 'react';
import './App.css';
import './libraries/materialize.min.css';

import Header from './components/Header.js'

import record from './images/record.png';
import Record from './views/Record';
import upload from './images/upload.png';
import Upload from './views/Upload';
import analytics from './images/analytics.png';
import Analytics from './views/Analytics';

class App extends Component {
  state = {
    screen: "home"
  };

  componentDidMount() {
    // Call our fetch function below once the component mounts
  }

  changeScreen(sStr) {
    console.log(sStr);
    this.setState({screen: sStr});
  }

  render() {
    if (this.state.screen === "home") {
      return (
        <React.Fragment>
          <br></br>
          <br></br>
          <div className="row">
            <div className="col l6 s10 offset-l3 offset-s1">
              <h1 align="center">dscribe</h1>
            </div>
          </div>
          <br></br>
          <div className="row">
            <div className="col l2 offset-l3 s12">
              <a onClick={() => this.changeScreen("record")}><img className="round icon clickable" src={record} alt="record"></img></a>
              <h4 align="center">Record</h4>
            </div>
            <div className="col l2 s12">
              <a onClick={() => this.changeScreen("upload")}><img className="round icon clickable" src={upload} alt="upload"></img></a>
              <h4 align="center">Upload</h4>
            </div>
            <div className="col l2 s12">
              <a onClick={() => this.changeScreen("analytics")}><img className="round icon clickable" src={analytics} alt="analytics"></img></a>
              <h4 align="center">Analyze</h4>
            </div>
          </div>
        </React.Fragment>
      );
    } else if (this.state.screen === "record") {
      return (
        <React.Fragment>
          <Header />
          <Record />
        </React.Fragment>
      );
    } else if (this.state.screen === "upload") {
      return (
        <React.Fragment>
          <Header />
          <Upload />
        </React.Fragment>
      );
    } else if (this.state.screen === "analytics") {
      return (
        <React.Fragment>
          <Header />
          <Analytics />
        </React.Fragment>
      );
    } else {
      return null;
    }
  }
}

export default App;
