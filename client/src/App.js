import React, { Component } from 'react';
import Analytics from './views/Analytics.js';
import './App.css';

class App extends Component {
  state = {
    data: null
  };

  componentDidMount() {
      // Call our fetch function below once the component mounts
    this.callBackendAPI()
      .then(res => this.setState({ data: res.express })).then((data) => console.log(data))
      .catch(err => console.log(err));
  }
  // sample backend API call
  callBackendAPI = async () => {
    const response = await fetch('/express_backend');
    const body = await response.json();
    console.log(body);

    if (response.status !== 200) {
      throw Error(body.message) 
    }
    return body;
  };

  render() {
    return (
      <div className="App">
        <Analytics />
      </div>
    );
  }
}

export default App;
