import React from 'react';
import {Bar} from 'react-chartjs-2';

class BarWithStyles extends React.Component {
  render() {
    const styles = {
      backgroundColor: 'rgba(255,99,132,0.2)',
      borderColor: 'rgba(255,99,132,1)',
      borderWidth: 1,
      hoverBackgroundColor: 'rgba(255,99,132,0.4)',
      hoverBorderColor: 'rgba(255,99,132,1)',
    }
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

BarWithStyles.defaultProps = {
  title: "No Title",
  data: [],
}

export default BarWithStyles;
