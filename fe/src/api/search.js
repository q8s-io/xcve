// 监控设置
import { get } from "@/helper/http/index.js";

/*
 * 获取
 */
export const getSuggest = params => {
  return get(`http://docker1001.idp.shyc2.qihoo.net:8099/sug`, params);
};

/*
 * 获取
 */
export const getDetail = params => {
  return get(`http://docker1001.idp.shyc2.qihoo.net:8099/cve`, params);
};

/*
 * 获取
 */
export const getConf = params => {
  return get(`http://docker1001.idp.shyc2.qihoo.net:8099/frontconf`, params);
};
