import React, { Component } from 'react';
import '../App.css'

class Record extends Component {
  state = {
    recorder: null,
    audio: null
  }

  /* https://medium.com/@bryanjenningz/how-to-record-and-play-audio-in-javascript-faa1b2b3e49b */
  recordAudio = () =>
    new Promise(async resolve => {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      const audioChunks = [];
      mediaRecorder.addEventListener("dataavailable", event => {
        audioChunks.push(event.data);
      });
      const start = () => mediaRecorder.start();
      const stop = () =>
        new Promise(resolve => {
          mediaRecorder.addEventListener("stop", () => {
            const audioBlob = new Blob(audioChunks);
            const audioUrl = URL.createObjectURL(audioBlob);
            const audio = new Audio(audioUrl);
            const play = () => audio.play();
            this.state.audio = audio;
            console.log(this.state.audio);

            resolve({ audioBlob, audioUrl, play });
          });
          mediaRecorder.stop();
        });
      resolve({ start, stop });
    });

  recordStop = async () => {
    if (this.state.recorder) {
      await this.state.recorder.stop();
      this.state.recorder = null;
      document.querySelector("#record-stop-button").textContent = "Record";
    } else {
      this.state.recorder = await this.recordAudio();
      this.state.recorder.start();
      document.querySelector("#record-stop-button").textContent = "Stop";
    }
  };

  render() {
    return (
      <React.Fragment>
        <div className="centered">
          <a onClick={this.recordStop} id="record-stop-button">Record</a>
        </div>
      </React.Fragment>
    );
  }
}

export default Record;