var webpack = require('webpack');
var path = require('path');

module.exports = {
  entry: [
    './app/static/js/app.js'  
  ],
  output: {
    path: path.join(__dirname, 'public/js'),
    filename: 'app.js'
  },
  module: {
    loaders: [
      {
        test: /\.js$/,
              loader: 'babel',
        query: {
          presets: ['es2015', 'react']
        },
        exclude: /node_modules/,
        include: path.join(__dirname, 'src')
      }
    ]
  }
};
