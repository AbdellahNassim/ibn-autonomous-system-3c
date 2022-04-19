const ROUTES = [
  {
    url: '/free',
    rateLimit: {
      windowMs: 15 * 60 * 1000,
      max: 5,
    },
    proxy: {
      target: 'https://www.google.com',
      changeOrigin: true,
      pathRewrite: {
        [`^/free`]: '',
      },
    },
  },
  {
    url: '/premium',
    proxy: {
      target: 'https://www.google.com',
      changeOrigin: true,
      pathRewrite: {
        [`^/premium`]: '',
      },
    },
  },
];

exports.ROUTES = ROUTES;
