const browsers = require("./browsers");

module.exports = {
  babelrc: false,
  presets: [
    [
      "@babel/preset-env",
      {
        loose: true,
        modules: false,
        targets: { browsers },
        exclude: [
          "@babel/plugin-transform-regenerator",
          "@babel/plugin-transform-typeof-symbol"
        ]
      }
    ]
  ],
  plugins: [
    "babel-plugin-transform-object-assign",
    "babel-plugin-proposal-decorators", // replaces legacy decorators
    ["@babel/plugin-transform-react-jsx", { pragma: "h" }]
  ]
};