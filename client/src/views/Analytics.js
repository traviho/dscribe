import React, { Component } from 'react';
import Select from 'react-select';
import {getColorUtil} from '../utils/GetColorUtil.js';
import BarWithTitle from '../charts/BarWithTitle.js';
import PieWithTitle from '../charts/PieWithTitle.js';
import LineWithTitle from '../charts/LineWithTitle.js';
import BubbleWithTitle from '../charts/BubbleWithTitle.js';

class Analytics extends Component {
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
    speakerPercentageData: {
        labels: [
            'Calvin',
            'Richard',
            'Wilson'
        ],
        datasets: [{
            data: [.33, .34, .33],
            backgroundColor: getColorUtil(3),
            hoverBackgroundColor: getColorUtil(3)
        }]
    },
    // timeSentimentData: {
    //     labels: ['10 mins', '20 mins', '30 mins', '40 mins', '50 mins', '1 hr'],
    //     datasets: [
    //       {
    //         label: 'My First dataset',
    //         fill: false,
    //         lineTension: 0.1,
    //         backgroundColor: 'rgba(75,192,192,0.4)',
    //         borderColor: 'rgba(75,192,192,1)',
    //         borderCapStyle: 'butt',
    //         borderDash: [],
    //         borderDashOffset: 0.0,
    //         borderJoinStyle: 'miter',
    //         pointBorderColor: 'rgba(75,192,192,1)',
    //         pointBackgroundColor: '#fff',
    //         pointBorderWidth: 1,
    //         pointHoverRadius: 5,
    //         pointHoverBackgroundColor: 'rgba(75,192,192,1)',
    //         pointHoverBorderColor: 'rgba(220,220,220,1)',
    //         pointHoverBorderWidth: 2,
    //         pointRadius: 1,
    //         pointHitRadius: 10,
    //         data: [0.5, 0.7, 0.6, 0.8, 0.2, -0.1, -0.4]
    //       }
    //     ]
    //   },
    //   sentimentQuestionFrequencySpeechPercentageData: {
    //     labels: ['Calvin', 'Travis'],
    //     datasets: [
    //       {
    //         label: 'My First dataset',
    //         fill: false,
    //         lineTension: 0.1,
    //         backgroundColor: 'rgba(75,192,192,0.4)',
    //         borderColor: 'rgba(75,192,192,1)',
    //         borderCapStyle: 'butt',
    //         borderDash: [],
    //         borderDashOffset: 0.0,
    //         borderJoinStyle: 'miter',
    //         pointBorderColor: 'rgba(75,192,192,1)',
    //         pointBackgroundColor: '#fff',
    //         pointBorderWidth: 1,
    //         pointHoverRadius: 5,
    //         pointHoverBackgroundColor: 'rgba(75,192,192,1)',
    //         pointHoverBorderColor: 'rgba(220,220,220,1)',
    //         pointHoverBorderWidth: 2,
    //         pointRadius: 1,
    //         pointHitRadius: 10,
    //         data: [{x:2,y:0.1,r:40}, {x:3,y:0.7,r:25}]
    //       }
    //     ]
    //   },
      selectedMeeting: null,
      selectedPerson: null,
  };

  handlePersonSelectChange = (selectedPerson) => {
    this.setState({ selectedPerson: selectedPerson });
  }

  handleMeetingSelectChange = (selectedMeeting) => {
    this.setState({ selectedMeeting: selectedMeeting });
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
            options={[
                { value: 'Richard', label: 'Richard' },
                { value: 'Wilson', label: 'Wilson' },
                { value: 'Calvin', label: 'Calvin' },
                { value: 'Travis', label: 'Travis' }
            ]}
            placeholder="Enter person(s)"
          />
        </div>
        <div className="col l2 s12" style={{paddingTop: '40px'}}>
          <Select
              value={this.state.selectedMeeting}
              onChange={this.handleMeetingSelectChange}
              isMulti={true}
              options={[
                  { value: 'Meeting 2/1/17 5pm', label: 'Meeting 2/1/17 5pm' },
                  { value: 'Meeting 1/12/17 2pm', label: 'Meeting 1/12/17 2pm' },
                  { value: 'Meeting 2/1/16 5pm', label: 'Meeting 2/1/16 5pm' }
              ]}
              placeholder="Enter meeting(s)"
          />
        </div>
      </div>
      <br />
      <div className="row">
        <div className="col l8 offset-l2 s12">
          <BarWithTitle data={this.state.wordFrequencyData} title="Keyword Frequency" />
        </div>
      </div>
      <br />
      <div className="row">
        <div className="col l8 offset-l2 s12">
          <PieWithTitle data={this.state.speakerPercentageData} title="Speaker Percentage" />
          {/* <LineWithTitle data={this.state.timeSentimentData}/>
          <BubbleWithTitle data={this.state.sentimentQuestionFrequencySpeechPercentageData}/> */}
        </div>
      </div>
      </React.Fragment>
    );
  }
}

export default Analytics;