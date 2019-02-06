import React, { Component } from 'react';
import Select from 'react-select';
import {getColorUtil} from '../utils/GetColorUtil.js';
import BarWithTitle from '../charts/BarWithStyles.js';
import PieWithStyles from '../charts/PieWithStyles.js';
import LineWithTitle from '../charts/LineWithTitle.js';
import BubbleWithTitle from '../charts/BubbleWithTitle.js';

class Analytics extends Component {

  /*
    meeting {
      name: "",
      value: 0,
      date: "",
      key_word_dict: {}
    }

    user {
      username: "",
      value: 0,
    }
  */

  state = {
    wordFrequencyData: {
        labels: ['Sprout', 'Hentai', 'Django', 'Scribe'],
        datasets: [
          {
            label: 'Word Frequency',
            backgroundColor: 'rgba(255,99,132,0.2)',
            borderColor: 'rgba(255,99,132,1)',
            borderWidth: 1,
            hoverBackgroundColor: 'rgba(255,99,132,0.4)',
            hoverBorderColor: 'rgba(255,99,132,1)',
            data: [1, 8, 4, 3]
          }
        ]
    },
    speakerPercentageData: {},
    selectedMeeting: null,
    selectedPerson: null,
    meetings: [],
    users: [],
  };

  componentDidMount() {
    this.populateUsers();
    this.populateMeetings();
    this.getSpeakerPercentageData();
  }

  handlePersonSelectChange = (selectedPerson) => {
    console.log(selectedPerson);
    this.setState({ selectedPerson: selectedPerson });
  }

  handleMeetingSelectChange = (selectedMeeting) => {
    console.log(selectedMeeting);
    this.setState({ selectedMeeting: selectedMeeting });
  }

  populateUsers = async() => {
    // value: userJSON.url.replace( /^\D+/g, '')
    const response = await fetch("http://localhost:8000/users/");
    const body = await response.json();
    const users = body.map((userJSON, index) => {
      return {
        username: userJSON.username,
        value: body.length - index,
      };
    });
    this.setState({users})
  }

  populateMeetings = async() => {
    const response = await fetch("http://localhost:8000/meeting/");
    const body = await response.json();
    const meetings = body.map(meetingJSON => {
      return {
        name: meetingJSON.name,
        value: meetingJSON.meeting_id,
        date: meetingJSON.date,
        key_word_dict: meetingJSON.key_word_dict,
      };
    });
    console.log(meetings);
    this.setState({meetings})
  }

  getSpeakerPercentageData = async() => {
    const response = await fetch(`http://localhost:8000/get-speaker-percentage?user=${1}&meeting=${1}`);
    const body = await response.json();
    const labels = Object.keys(body);
    //labels.push('fake', 'data');
    const values = Object.values(body);
    //values.push(4, 3);
    const sumReducer = (acc, i) => acc + i;
    const totalWords = values.reduce(sumReducer);
    const data = values.map(val => val / totalWords);
    
    this.setState({speakerPercentageData: {
      labels,
      datasets: [{data,}],
    }});
  }

  getSelectionFromUsersState() {
    return this.state.users.map(userObj => {
      return {
        value: userObj.value,
        label: userObj.username
      }
    })
  }

  getSelectionFromMeetingState() {
    return this.state.meetings.map(meetingObj => {
      return {
        value: meetingObj.value,
        label: meetingObj.name + " " + meetingObj.date
      }
    })
  }

  getAggregateKeywordFrequencyFromMeetings() {
    let keyCounts = {};
    for (var keyMeeting in this.state.meetings) {
      let meeting = this.state.meetings[keyMeeting]
      for (var keyWord in meeting.key_word_dict) {
        keyCounts[keyWord] = keyCounts[keyWord] == undefined ? meeting.key_word_dict[keyWord] : keyCounts[keyWord] + meeting.key_word_dict[keyWord];
      }
    }
    return {
      labels: Object.keys(keyCounts),
      datasets: [
        {
          label: "Word Frequency",
          data: Object.keys(keyCounts).map(function(key){
            return keyCounts[key];
          }),
        }
      ]
    }
  }

  render() {
    return (
      <React.Fragment>
        <div className="row">
          <div className="col l5 offset-l1 s0">
            <h2>Meeting Analytics</h2>
          </div>
          <div className="col l2 offset-l1 s12" style={{paddingTop: '40px'}}>
            <Select
              value={this.state.selectedPerson}
              onChange={this.handlePersonSelectChange}
              isMulti={true}
              options={this.getSelectionFromUsersState()}
              placeholder="Enter person(s)"
            />
          </div>
          <div className="col l2 s12" style={{paddingTop: '40px'}}>
            <Select
                value={this.state.selectedMeeting}
                onChange={this.handleMeetingSelectChange}
                isMulti={true}
                options={this.getSelectionFromMeetingState()}
                placeholder="Enter meeting(s)"
            />
          </div>
        </div>
        <br />
        <div className="row">
          <div className="col l8 offset-l2 s12">
            <BarWithTitle data={this.getAggregateKeywordFrequencyFromMeetings()} title="Keyword Frequency" />
          </div>
        </div>
        <br />
        <div className="row">
          <div className="col l8 offset-l2 s12">
            <PieWithStyles data={this.state.speakerPercentageData} title="Speaker Percentage" />
            {/* <LineWithTitle data={this.state.timeSentimentData}/>
            <BubbleWithTitle data={this.state.sentimentQuestionFrequencySpeechPercentageData}/> */}
          </div>
        </div>
      </React.Fragment>
    );
  }
}

export default Analytics;
