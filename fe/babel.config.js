module.exports = {
  presets: [
    [
      "@vue/app",
      {
        polyfills: [
          "es6.promise",
          "es6.array.find-index",
          "es6.array.find",
          "es7.array.includes",
          "es6.string.includes",
          "es6.string.find"
        ]
      }
    ]
  ]
};
