// 监控设置
import { get } from "@/helper/http/index.js";

/*
 * 获取
 */
export const getSuggest = params => {
  return get(`/sug`, params);
};

/*
 * 获取
 */
export const getDetail = params => {
  return get(`/cve`, params);
};

/*
 * 获取
 */
export const getConf = params => {
  return get(`/frontconf`, params);
};
