const express = require('express');
const morgan = require('morgan');
const {createProxyMiddleware} = require('http-proxy-middleware');
const {ROUTES} = require('./routes');


const app = express();

// set up morgan for logging
app.use(morgan('combined'));


const port = 3000;


ROUTES.forEach((r) => {
  app.use(r.url, createProxyMiddleware(r.proxy));
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});
