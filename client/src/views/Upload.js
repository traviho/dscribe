import React, { Component } from 'react';
import '../App.css'
import axios from 'axios';

class Upload extends Component {
  constructor(props) {
    super(props);
  }

  handleSubmit = (event) => {
    event.preventDefault();
    var formData = new FormData();
    var audiofile = document.querySelector('#afile');
    formData.append("audio", audiofile.files[0]);
    axios.post('/audio',
               formData,
               {headers: {'Content-Type': 'multipart/form-data'}}).then(() => this.props.screenHandler('analytics'));
  }

  render() {
    return (
      <React.Fragment>
        <br></br>
        <div className="row">
          <div className="col l6 offset-l3 s12">
             <form onSubmit={this.handleSubmit}>
                <div className="file-field input-field">
                  <div className="btn">
                    <span>Select File</span>
                    <input type="file" name="audio" accept="audio/*" id="afile" />
                  </div>
                  <div className="file-path-wrapper">
                    <input className="file-path validate" type="text" />
                  </div>
                </div>
                <input className='btn-large' type="submit" name="submit" value="upload" />
            </form>
          </div>
        </div>
      </React.Fragment>
    );
  }
}

export default Upload;
