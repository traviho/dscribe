import React from 'react';
import {Pie} from 'react-chartjs-2';

class PieWithTitle extends React.Component {
  render() {
    return (
      <div>
        <h2>{this.props.title}</h2>
        <Pie
          data={this.props.data}
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
