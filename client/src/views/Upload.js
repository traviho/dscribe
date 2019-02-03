import React, { Component } from 'react';
import '../App.css'
import axios from 'axios';
import CSRFToken from './csrftoken';

class Upload extends Component {
  // state = {
  //   selectedFile: null
  // }

  // handleSelectFile = (file) => {
  //   this.setState({ selectedFile: file });
  // }
  //
  // handleUpload = () => {
  //   const upload = new FormData()
  //   const endpoint = "/audio"
  //
  //   upload.append('file', this.state.selectedFile, this.state.selectedFile.name)
  //   axios.post(endpoint, upload);
  // }
  constructor(props) {
    super(props);
  }

  handleSubmit = (event) => {
    event.preventDefault();
    fetch('/audio').then(() => this.props.screenHandler('analytics'));
  }

  render() {
    return (
      <React.Fragment>
         <form onSubmit={this.handleSubmit}>
            <div className="file-field input-field">
              <div className="btn">
                <span>Select File</span>
                <input type="file" name="audio" accept="audio/*" />
              </div>
              <div className="file-path-wrapper">
                <input className="file-path validate" type="text" />
              </div>
            </div>
            <input className='btn-large' type="submit" name="submit" value="upload" />
        </form>
      </React.Fragment>
    );
  }
}

export default Upload;
