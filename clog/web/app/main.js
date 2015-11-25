import 'normalizecss/normalize.css';
import './base.css';

import $ from 'domtastic';
import ClogClient from './client';
import { ChartComponent as Chart } from './components';


// TODO: Figure out configuration handling.
var clog = new ClogClient();

$(document).ready(() => {
  let chart = new Chart({
    id: 'log-chart',
    height: 400,
    width: 800
  });

  clog.getLogs('summary', 300, (resp) => {
    let keys = Object.keys(resp.result),
        vals = keys.map(key => resp.result[key]);
    let data = {
      labels: keys,
      datasets: [
        {
          label: 'Count',
          data: vals
        }
      ]
    };
    $('#log-charts').append(chart);
    chart.update(data);
    chart.render();
  })
});
