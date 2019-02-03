import React from 'react';
import {Bar} from 'react-chartjs-2';

class BarWithTitle extends React.Component {
  render() {
    return (
      <div>
        <h4>{this.props.title}</h4>
        <Bar
          data={this.props.data}
          width={100}
          height={50}
          options={{
            maintainAspectRatio: false,
            legend: {
              position: 'bottom'
            }
          }}
        />
      </div>
    );
  }
}

BarWithTitle.defaultProps = {
  title: "No Title",
  data: [],
}

export default BarWithTitle;
