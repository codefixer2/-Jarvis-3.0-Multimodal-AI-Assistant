// loaders/cssLoaders.js
const autoprefixer = require("autoprefixer");

module.exports = (isProd) => {
  const cssLoaderOptions = {
    sourceMap: !isProd,
    importLoaders: 2, // postcss-loader + sass-loader
    modules: isProd
      ? { localIdentName: "[local]_[hash:base64:5]" }
      : { localIdentName: "[path][name]__[local]" }
  };

  const loaders = [];

  // In development, inject styles into DOM
  if (!isProd) {
    loaders.push({ loader: "style-loader" });
  } else {
    // In production, extract CSS to separate files
    const MiniCssExtractPlugin = require("mini-css-extract-plugin");
    loaders.push({ loader: MiniCssExtractPlugin.loader });
  }

  loaders.push(
    {
      loader: "css-loader",
      options: cssLoaderOptions
    },
    {
      loader: "postcss-loader",
      options: {
        sourceMap: !isProd,
        postcssOptions: {
          plugins: [
            autoprefixer() // Browserslist config is read automatically
          ]
        }
      }
    },
    {
      loader: "sass-loader",
      options: { sourceMap: !isProd }
    }
  );

  return loaders;
};