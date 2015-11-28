import reqwest from 'reqwest';

class ClogClient {
  constructor(serverUrl='') {
    this.serverUrl = serverUrl;
  }
  getLogs(format = '', interval = '', order_by = '-date', cb) {
    reqwest(`${this.serverUrl}/api/v1/logs/
?format=${format}&interval=${interval}&order_by=${order_by}`, cb);
  }
  getLog(id, cb) {
    reqwest(`${this.serverUrl}/api/v1/log/${id}`, cb);
  }
}

export default ClogClient;
