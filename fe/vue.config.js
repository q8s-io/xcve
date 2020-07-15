// vue.config.js
const path = require("path");
// const QCDN = require("@q/webpack-qcdn-file");

function resolve(dir) {
  return path.join(__dirname, dir);
}

module.exports = {
  outputDir: "../public/",
  assetsDir: "dist",
  transpileDependencies: ["vue-echarts", "resize-detector"],
  // publicPath: process.env.NODE_ENV === "production" ? "/public/" : "/",
  chainWebpack: config => {
    config.resolve.alias
      .set("@vue", resolve("src/vue"))
      .set("@assets", resolve("src/assets"))
      .set("@components", resolve("src/components"))
      .set("@api", resolve("src/api"))
      .set("@views", resolve("src/views"))
      .set("@config", resolve("src/config"))
      .set("@helper", resolve("src/helper"));
    const svgRule = config.module.rule("svg");
    svgRule.uses.clear();
    svgRule
      .test(/\.svg$/)
      .include.add(path.resolve(__dirname, "./src/assets/svg"))
      .end()
      .use("vue-svg-loader")
      .loader("vue-svg-loader");

    const fileRule = config.module.rule("file");
    fileRule.uses.clear();
    fileRule
      .test(/\.svg$/)
      .exclude.add(path.resolve(__dirname, "./src/assets/svg"))
      .end()
      .use("url-loader")
      .loader("url-loader");
  },
  configureWebpack: config => {
    config.entry.app = ["babel-polyfill", "./src/main.js"];
    if (process.env.NODE_ENV === "production") {
      // new QCDN();
    }
  },
  devServer: {
    port: 8111,
    proxy: {
      "/api": {
        target: "http://i6985.se.shbt.qihoo.net:1180",
        pathRewrite: { "^/api": "" }
      }
    },
    disableHostCheck: true
  }
};
