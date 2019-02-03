import React from 'react';
import {Line} from 'react-chartjs-2';

class LineWithTitle extends React.Component {
  render() {
    return (
      <div>
        <h2>{this.props.title}</h2>
        <Line
          data={this.props.data}
        />
      </div>
    );
  }
}

LineWithTitle.defaultProps = {
  title: "No Title",
  data: [],
}

export default LineWithTitle;
