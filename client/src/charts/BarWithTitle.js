import React from 'react';
import {Bar} from 'react-chartjs-2';

class BarWithTitle extends React.Component {
  render() {
    return (
      <div>
        <h2>{this.props.title}</h2>
        <Bar
          data={this.props.data}
          width={100}
          height={50}
          options={{
            maintainAspectRatio: false
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
