import React, { Component } from 'react';
import BarWithTitle from '../charts/BarWithTitle.js';

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
      }
  };

  render() {
    return (
      <div>
        <BarWithTitle data={this.state.wordFrequencyData}/>
      </div>
    );
  }
}

export default Analytics;