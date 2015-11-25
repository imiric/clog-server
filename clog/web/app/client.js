import reqwest from 'reqwest';

class ClogClient {
  constructor(serverUrl='') {
    this.serverUrl = serverUrl;
  }
  getLogs(format = '', interval = '', cb) {
    reqwest(`${this.serverUrl}/api/v1/logs/
?format=${format}&interval=${interval}`, cb);
  }
}

export default ClogClient;
