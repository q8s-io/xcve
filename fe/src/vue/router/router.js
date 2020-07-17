import Index from "@views/Index.vue";
import _Error from "@views/Error/index.vue";

import Main from "@views/Main";
import Search from "@views/Search";

const routers = [
  {
    path: "/",
    redirect: "/",
    component: Index,
    children: [
      {
        path: "/",
        name: "index",
        component: Main
      },
      {
        path: "/s",
        name: "s",
        component: Search
      }
    ]
  },
  { path: "*", component: _Error }
];

export default routers;
