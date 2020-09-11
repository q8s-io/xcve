// 监控设置
import { get } from "@/helper/http/index.js";

/*
 * 获取随机实体
 */
export const getRandom = params => {
  return get(`/sug`, params);
};

/*
 * 获取suggest
 */
export const getSuggest = params => {
  return get(`/sug`, params);
};

/*
 * 获取实体详情
 */
export const getDetail = params => {
  return get(`/search`, params);
};

/*
 * 获取配置信息
 */
export const getConf = params => {
  return get(`/frontconf`, params);
};
