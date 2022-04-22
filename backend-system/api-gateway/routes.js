const ROUTES = [
  {
    url: '/slices',
    proxy: {
      target: 'http://decision_maker',
      changeOrigin: true,
      pathRewrite: {
        [`^/slices`]: '',
      },
    },
  },
  
];

exports.ROUTES = ROUTES;
