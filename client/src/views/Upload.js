import React, { Component } from 'react';
import '../App.css'
import axios from axios;

class Upload extends Component {
  state = {
    selectedFile: null
  }

  handleSelectFile = (file) => {
    this.setState({ selectedFile: file })
  }

  handleUpload = () => {
    const upload = new FormData()
    const endpoint = "/audio"

    upload.append('file', this.state.selectedFile, this.state.selectedFile.name)
    axios.post(endpoint, upload);
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