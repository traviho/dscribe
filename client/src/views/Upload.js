import React, { Component } from 'react';
import '../App.css'

class Upload extends Component {
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
        <div className="centered">
          <input type="file" accept="audio/*" onChange={this.handleSelectFile} />
          <button onClick={this.handleUpload}>Upload</button>
        </div>
      </React.Fragment>
    );
  }
}

export default Upload;