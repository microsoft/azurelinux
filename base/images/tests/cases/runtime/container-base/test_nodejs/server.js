'use strict';

// Minimal stdlib HTTP server used to validate the Node.js runtime.
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8080;
const HOST = '0.0.0.0';
const RESPONSE = fs.readFileSync(path.join(__dirname, 'response.txt'));

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end(RESPONSE);
});

server.listen(PORT, HOST);
