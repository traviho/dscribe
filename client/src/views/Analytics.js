import React, { Component } from 'react';
import BarWithTitle from '../charts/BarWithTitle.js';
import PieWithTitle from '../charts/PieWithTitle.js';
import LineWithTitle from '../charts/LineWithTitle.js';

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
            backgroundColor: [
            '#FF6384',
            '#36A2EB',
            '#FFCE56'
            ],
            hoverBackgroundColor: [
            '#FF6384',
            '#36A2EB',
            '#FFCE56'
            ]
        }]
    },
    timeSentimentData: {
        labels: ['10 mins', '20 mins', '30 mins', '40 mins', '50 mins', '1 hr'],
        datasets: [
          {
            label: 'My First dataset',
            fill: false,
            lineTension: 0.1,
            backgroundColor: 'rgba(75,192,192,0.4)',
            borderColor: 'rgba(75,192,192,1)',
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            pointBorderColor: 'rgba(75,192,192,1)',
            pointBackgroundColor: '#fff',
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: 'rgba(75,192,192,1)',
            pointHoverBorderColor: 'rgba(220,220,220,1)',
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10,
            data: [0.5, 0.7, 0.6, 0.8, 0.2, -0.1, -0.4]
          }
        ]
      }
  };

  render() {
    return (
      <div>
        <BarWithTitle data={this.state.wordFrequencyData}/>
        <PieWithTitle data={this.state.speakerPercentageData}/>
        <LineWithTitle data={this.state.timeSentimentData}/>
      </div>
    );
  }
}

export default Analytics;