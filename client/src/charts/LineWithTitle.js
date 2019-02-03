import React from 'react';
import {Line} from 'react-chartjs-2';

class LineWithTitle extends React.Component {
  render() {
    return (
      <div>
        <h4>{this.props.title}</h4>
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
