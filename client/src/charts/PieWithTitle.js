import React from 'react';
import {Pie} from 'react-chartjs-2';

class PieWithTitle extends React.Component {
  render() {
    return (
      <div>
        <h4>{this.props.title}</h4>
        <Pie
          data={this.props.data}
          options={{
            legend: {
              position: 'bottom'
            }
          }}
        />
      </div>
    );
  }
}

PieWithTitle.defaultProps = {
  title: "No Title",
  data: [],
}

export default PieWithTitle;
