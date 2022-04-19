const ROUTES = [
  {
    url: '/decision_maker',
    proxy: {
      target: 'http://decision_maker',
      changeOrigin: true,
      pathRewrite: {
        [`^/decision_maker`]: '',
      },
    },
  },
  {
    url: '/data_contextualize',
    proxy: {
      target: 'http://data_contextualize',
      changeOrigin: true,
      pathRewrite: {
        [`^/data_contextualize`]: '',
      },
    },
  },
  {
    url: '/intent_monitor',
    proxy: {
      target: 'http://intent_monitor',
      changeOrigin: true,
      pathRewrite: {
        [`^/intent_monitor`]: '',
      },
    },
  },
  {
    url: '/policy_generator',
    proxy: {
      target: 'http://policy_generator',
      changeOrigin: true,
      pathRewrite: {
        [`^/policy_generator`]: '',
      },
    },
  },
];

exports.ROUTES = ROUTES;
