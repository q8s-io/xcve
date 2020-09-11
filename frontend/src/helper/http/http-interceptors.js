import axios from "axios";
import Qs from "qs";
import { prefix } from "@/config/index.js";
import { checkStatus } from "@helper/check.js";

/**
 * 请求配置
 * @see https://github.com/mzabriskie/axios
 */
const baseConfig = Object.freeze({
  timeout: 60000, // 请求超时时间
  // withCredentials: true, // 跨域
  baseURL: prefix
});

const instance = axios.create(baseConfig);

instance.interceptors.request.use(
  config => {
    const resetMethods = ["post", "put"];
    const currentMethod = config.method.toLocaleLowerCase();

    if (resetMethods.includes(currentMethod)) {
      const contentType = config.headers["Content-Type"];
      // 根据Content-Type转换data格式
      if (contentType) {
        if (contentType.includes("multipart")) {
          // 类型 'multipart/form-data;'
        } else if (contentType.includes("json")) {
          // 类型 'application/json;'
          // 服务器收到的raw body(原始数据) "{name:"nowThen",age:"18"}"（普通字符串）
          config.data = JSON.stringify(config.data);
        } else {
          // 类型 'application/x-www-form-urlencoded;'
          // 服务器收到的raw body(原始数据) name=nowThen&age=18
          config.data = Qs.stringify(config.data);
        }
      }
    }

    return config;
  },
  error => {
    Promise.reject(error);
  }
);

instance.interceptors.response.use(
  response => {
    if (response.config.responseType === "blob") return response;
    return checkStatus(response);
  },
  error => {
    console.log(2);
    return checkStatus(error.response);
  }
);

export default instance;
