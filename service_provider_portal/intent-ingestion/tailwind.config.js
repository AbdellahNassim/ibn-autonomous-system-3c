const plugin = require('tailwindcss/plugin');

module.exports = {
  content: [
    './index.html',
    './src/**/*.{js,jsx,ts,tsx}',
  ],
  theme: {
    extend: {
      boxShadow: {
        DEFAULT: '0 1px 3px 0 rgba(0, 0, 0, 0.08), 0 1px 2px 0 rgba(0, 0, 0, 0.02)',
        md: '0 4px 6px -1px rgba(0, 0, 0, 0.08), 0 2px 4px -1px rgba(0, 0, 0, 0.02)',
        lg: '0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.01)',
        xl: '0 20px 25px -5px rgba(0, 0, 0, 0.08), 0 10px 10px -5px rgba(0, 0, 0, 0.01)',
      },
      outline: {
        blue: '2px solid rgba(0, 112, 244, 0.5)',
      },
      fontFamily: {
        inter: ['Inter', 'sans-serif'],
      },
      colors: {
        'primary': {
          '50': '#3cc8ff',
          '100': '#32beff',
          '200': '#28b4ff',
          '300': '#1eaaff',
          '400': '#14a0ff',
          '500': '#0a96fd',
          '600': '#008cf3',
          '700': '#0082e9',
          '800': '#0078df',
          '900': '#006ed5',
        },
        'grey': {
          '50': '#b2b2b2',
          '100': '#a8a8a8',
          '200': '#9e9e9e',
          '300': '#949494',
          '400': '#8a8a8a',
          '500': '#808080',
          '600': '#767676',
          '700': '#6c6c6c',
          '800': '#626262',
          '900': '#585858',
        },
        'red': {
          '50': '#ff6565',
          '100': '#ff5b5b',
          '200': '#ff5151',
          '300': '#ff4747',
          '400': '#ff3d3d',
          '500': '#ff3333',
          '600': '#f52929',
          '700': '#eb1f1f',
          '800': '#e11515',
          '900': '#d70b0b',
        },
        'purple': '#7e5bef',
        'pink': '#ff49db',
        'orange': '#ff7849',
        'green': '#13ce66',
        'yellow': '#ffc82c',
        'gray-dark': '#273444',
        'gray': '#8492a6',
        'gray-light': '#d3dce6',

        'black': {
          lighter: '#212121',
          default: '#2D2D2D',
          darker: '#000000',
        },
      },
      fontSize: {
        'xs': ['0.75rem', {lineHeight: '1.5'}],
        'sm': ['0.875rem', {lineHeight: '1.5715'}],
        'base': ['1rem', {lineHeight: '1.5', letterSpacing: '-0.01em'}],
        'lg': ['1.125rem', {lineHeight: '1.5', letterSpacing: '-0.01em'}],
        'xl': ['1.25rem', {lineHeight: '1.5', letterSpacing: '-0.01em'}],
        '2xl': ['1.5rem', {lineHeight: '1.33', letterSpacing: '-0.01em'}],
        '3xl': ['1.88rem', {lineHeight: '1.33', letterSpacing: '-0.01em'}],
        '4xl': ['2.25rem', {lineHeight: '1.25', letterSpacing: '-0.02em'}],
        '5xl': ['3rem', {lineHeight: '1.25', letterSpacing: '-0.02em'}],
        '6xl': ['3.75rem', {lineHeight: '1.2', letterSpacing: '-0.02em'}],
      },
      screens: {
        xs: '480px',
      },
      borderWidth: {
        3: '3px',
      },
      minWidth: {
        36: '9rem',
        44: '11rem',
        56: '14rem',
        60: '15rem',
        72: '18rem',
        80: '20rem',
      },
      maxWidth: {
        '8xl': '88rem',
        '9xl': '96rem',
      },
      zIndex: {
        60: '60',
      },
    },
  },
  plugins: [
    // eslint-disable-next-line global-require
    require('@tailwindcss/forms'),
    // add custom variant for expanding sidebar
    plugin(({addVariant, e}) => {
      addVariant('sidebar-expanded', ({modifySelectors, separator}) => {
        modifySelectors(({className}) => `.sidebar-expanded .${e(`sidebar-expanded${separator}${className}`)}`);
      });
    }),
  ],
};
