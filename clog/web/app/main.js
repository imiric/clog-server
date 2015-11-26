import 'normalizecss/normalize.css';
import './base.css';

import $ from 'domtastic';
import ClogClient from './client';
import { ChartComponent as Chart, Table } from './components';


// TODO: Figure out configuration handling.
var clog = new ClogClient();

$(document).ready(() => {
  let chart = new Chart({
    id: 'log-chart',
    height: 400,
    width: 800
  });
  let table = new Table($('<table><tr><th>ID</th><th>Date</th></tr></table>'));

  clog.getLogs('summary', 300, undefined, (resp) => {
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
  });

  // XXX: Is there a way of setting just one argument by name in ES6?
  // E.g. `getLogs(cb=(resp) => ...)`.
  clog.getLogs(undefined, undefined, undefined, (resp) => {
    $('#log-list').append(table);
    resp.result.forEach((el, idx) => {
      table.append(`<tr><td>${el.id}</td><td>${el.date}</td></tr>`);
    });
  });
});
