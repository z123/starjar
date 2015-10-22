var ExtractTextPlugin = require('extract-text-webpack-plugin');

var assetsjs = './app/static/js/entry.js'
var assetscss = './app/static/css/entry.scss'

module.exports = {
  entry: [
      assetsjs,
      assetscss
  ],
  output: {
    path: './dist',
    filename: 'bundle.js'
  },            
  module: {
    loaders: [
      {
        test: /\.scss$/,
        loader: ExtractTextPlugin.extract("style-loader", "css-loader!sass-loader")
      }
    ]
  },
  plugins: [
    new ExtractTextPlugin("styles.css")
  ]
}

