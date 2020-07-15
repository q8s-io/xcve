import filters from "./filters";

const importFilters = Vue => {
  Vue.filter("format", filters.format);
};

export default importFilters;
