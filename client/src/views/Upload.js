import React, { Component } from 'react';
import '../App.css'
import axios from 'axios';
import CSRFToken from './csrftoken';

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
         <form action="/audio" method="POST" enctype="multipart/form-data">
            <CSRFToken />
            <div className="file-field input-field">
              <div className="btn">
                <span>Select File</span>
                <input type="file" name="audio" accept="audio/*" />
              </div>
              <div class="file-path-wrapper">
                <input className="file-path validate" type="text" />
              </div>
            </div>
            <input className='btn-large' type="submit" name="submit" value="audio" />
        </form>
      </React.Fragment>
    );
  }
}

export default Upload;
