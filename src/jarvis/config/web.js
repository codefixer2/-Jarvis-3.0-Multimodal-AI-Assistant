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

module