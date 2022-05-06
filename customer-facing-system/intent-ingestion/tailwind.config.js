module.exports = {
  content: [
    './src/**/*.{js,jsx,ts,tsx}',
  ],
  theme: {
    extend: {},
    fontFamily: {
      sans: ['Roboto Mono', 'Cairo', 'Open Sans', 'sans-serif'],
    },
    colors: {
      black: {
        lighter: '#212121',
        default: '#2D2D2D',
        darker: '#000000',
      },
      white: {
        lighter: '#FFFFFF',
        default: '#F8F9FA',
      },
    },
  },
  plugins: [],
};
