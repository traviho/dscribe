import React from 'react';
import {Bubble} from 'react-chartjs-2';

class BubbleWithTitle extends React.Component {
  optionsData = {
    scales: {
      yAxes: [{
        ticks: {
          max: 1,
          min: -1,
          stepSize: 0.25
        },
        scaleLabel: {
          display: true,
          labelString: 'Sentiment'
        }
      }],
      xAxes: [{
        ticks: {
          max: 10,
          min: 0,
          stepSize: 1
        },
        scaleLabel: {
          display: true,
          labelString: 'Number of Questions'
        }
      }],
    }
  };

  render() {
    return (
      <div>
        <h2>{this.props.title}</h2>
        <Bubble
          data={this.props.data} options={this.optionsData}
        />
      </div>
    );
  }
}

BubbleWithTitle.defaultProps = {
  title: "No Title",
  data: {},
}

export default BubbleWithTitle;
