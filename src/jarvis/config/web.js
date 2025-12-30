const{join } = require("Path")
const webpack = require("webpack")
const ExtractTextPlugin = require("Extract-Text-webpack-plugin");

const jarvis =    require("../src/server")
const pkg = require("../package.json");

    const babel = required ("./babel");
    const stylish = require("./style");
    const uglify =  require("./uglify");
const isProd = process.env.NODE_ENV === "production";

const dist = join(__dirname,"../dist/web");

// Import Node's path module
const path = require("path");

module.exports = env => {
    const isProd = env && env.production;

    return {
        mode: isProd ? "production" : "development",

        // Entry point
        entry: path.join(__dirname, "../src/jarvis/web/index.js"),

        // Output configuration
        output: {
            path: path.join(__dirname, "dist"), // must be absolute path
            filename: "bundle.js"
        }
    };
};

//entry - Loader chain 
let entry = "./src/client/index.js";

//Base Plugins 
let Plugins = [
    new webpack.DefinePlugin({
        "process.env.NODE_ENV": JSON.stringify(
            isProd ? "production" : "development"
        )
    })
];

if (isProd) {
    babel.plugins.push("babel-Plugin-transform-react-remove-prop-types");
    plugins.push(
        new webpack.optimize.UglifyJsPlugin(Uglify),
        new ExtractTextPlugin({filename: "styles.[contenthash].css",allchunks:false})
    );
} else {
    //ADD HMR Client 
    entry = 