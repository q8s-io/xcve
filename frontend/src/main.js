import Vue from "vue";
import App from "./App.vue";
//import "view-design/dist/styles/iview.css";
// import "../src/assets/css/iview.css";
import "./theme/index.less";

import router from "@vue/router/index.js";
import store from "@vue/store/index.js";

import importFilters from "@vue/filters/index.js";
import importDirectives from "@vue/directives/index.js";

import components from "@components/basic/index.js";

importFilters(Vue);
importDirectives(Vue);

Vue.use(components);

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
