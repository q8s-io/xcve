import { Message } from "iview";

// 此时设定返回data notrycatch代表代码状态码需要特别处理 否则错误处理直接在这里
export function checkStatus(response) {
  let { status, config, data } = response;

  let errorMsg = "网络异常~";
  if (config.notrycatch) {
    return Promise.resolve(data);
  } else {
    if (status !== 200) {
      Message.error({
        content: errorMsg
      });

      return Promise.resolve(response.data);
    } else {
      // if (data && (data.errno === 0 || data.error === 0)) {
      //   return Promise.resolve(data);
      // } else {
      //   Message.error({
      //     content: data.msg || errorMsg
      //   });

      //   return Promise.reject(data);
      // }
      return Promise.resolve(data);
    }
  }
}
