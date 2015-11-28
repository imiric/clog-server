import $ from 'domtastic';

import ClogClient from './client';
import { ChartComponent as Chart, Table } from './components';

// TODO: Figure out configuration handling.
var clog = new ClogClient();

export function index() {
  $('#content').empty();
  $('#content').append('<h2>Log events</h2>');
  $('#content').append('<div id="log-charts"/>');
  $('#content').append('<div id="log-list"/>');

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
      let link = `<a href="/log/${el.id}">${el.id}</a>`;
      table.append(`<tr><td>${link}</td><td>${el.date}</td></tr>`);
    });
  });
}

export function log(ctx) {
  let c = $(container),
      logId = ctx.params.id;

  c.empty();
  c.append(`<h3>Log ${logId}</h3>`);
  clog.getLog(logId, (resp) => {
    c.append('<h5>Date</h5>');
    c.append(`<p>${resp.date}</p>`);
    c.append('<h5>Source</h5>');
    c.append(`<p>${resp.source}</p>`);
    c.append('<h5>Data</h5>');
    c.append(`<p>${resp.log.data}</p>`);
  });
}
