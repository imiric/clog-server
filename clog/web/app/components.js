import $ from 'domtastic';
import Chart from 'chart.js';
import merge from 'lodash.merge';


export class ChartComponent extends $.BaseClass {
  constructor(options) {
    let el = $(`<canvas id="${options.id}" width="${options.width}"
                height="${options.height}"></canvas>`);
    super(el);
    this.el = el;
    this.chart = null;
    this.data = options.data || {};
    this.chartOptions = options.chartOptions || {
      fillColor: "rgba(151,187,205,0.2)",
      strokeColor: "rgba(151,187,205,1)",
      pointColor: "rgba(151,187,205,1)",
      pointStrokeColor: "#fff",
      pointHighlightFill: "#fff",
      pointHighlightStroke: "rgba(151,187,205,1)",
    }
  }
  render() {
    if (this.chart === null) {
      let ctx = this.el.get(0).getContext('2d');
      this.chart = new Chart(ctx).Line(this.data);
    } else {
      // TODO: Update the data before rendering.
      this.chart.update();
    }
  }
  update(data) {
    data.datasets[0] = merge(data.datasets[0], this.chartOptions);
    this.data = data;
  }
}
