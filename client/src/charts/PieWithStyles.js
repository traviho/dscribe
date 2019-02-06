import React from 'react';
import {Pie} from 'react-chartjs-2';
import {getColorUtil} from '../utils/GetColorUtil.js';

class PieWithStyles extends React.Component {
  render() {
    const data = this.props.data;
    if (data === undefined || data === null | data.datasets === undefined || data.datasets === null) {
      return null;
    }
    data.datasets.forEach((dataset) => {
      console.log(dataset)
      dataset['backgroundColor'] = getColorUtil(data.labels.length);
    });
    return (
      <div>
        <h4>{this.props.title}</h4>
        <Pie
          data={data}
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

PieWithStyles.defaultProps = {
  title: "No Title",
  data: [],
}

export default PieWithStyles;
