import React, { Component } from 'react';
import '../App.css'

class Analytics extends Component {
  state = {
    selectedFile: null
  }

  handleSelectFile = (file) => {
    this.setState({ selectedFile: file })
  }

  handleUpload = () => {
    console.log("Upload");
  }

  render() {
    return (
      <React.Fragment>
        <div class="centered">
          <input type="file" accept="audio/*" onChange={this.handleSelectFile} />
          <button onClick={this.handleUpload}>Upload</button>
        </div>
      </React.Fragment>
    );
  }
}

export default Analytics;