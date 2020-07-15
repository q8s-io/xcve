import Index from "@views/Index.vue";
import _Error from "@views/Error/index.vue";

import Main from "@views/Main";
import Search from "@views/Search";

const routers = [
  {
    path: "/",
    redirect: "/index",
    component: Index,
    children: [
      {
        path: "/index",
        name: "index",
        component: Main
      },
      {
        path: "/search",
        name: "search",
        component: Search
      }
    ]
  },
  { path: "*", component: _Error }
];

export default routers;
