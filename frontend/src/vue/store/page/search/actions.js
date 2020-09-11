import { getList } from "@api/search.js";
import { page_size } from "@/config/index.js";
export default {
  async getList({ dispatch }, params) {
    await getList(params);
    dispatch("getList", { page_no: 1, page_size: page_size });
  }
};
