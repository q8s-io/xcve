import directives from "./directives";

const importDirectives = Vue => {
  Vue.directive("focus", directives.focus);
};

export default importDirectives;
