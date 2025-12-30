const TerserPlugin = require('terser-webpack-plugin');

module.exports = {
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          format: {
            comments: false, // remove all comments
          },
          mangle: true,
          compress: {
            properties: true,
            keep_fargs: false,
            pure_getters: true,
            collapse_vars: true,
            warnings: false,
            ie8: false, // replaces screw_ie8
            sequences: true,
            dead_code: true,
            drop_debugger: true,
            comparisons: true,
            conditionals: true,
            evaluate: true,
            booleans: true,
            loops: true,
            unused: true,
            hoist_funs: true,
            if_return: true,
            join_vars: true,
            drop_console: false,
            pure_funcs: [
              "classCallCheck",
              "_classCallCheck",
              "_possibleConstructorReturn",
              "Object.freeze",
              "invariant",
              "warning"
            ]
          }
        },
        extractComments: false // don't generate separate LICENSE.txt
      })
    ]
  }
};
