const CURRENT_DOMAIN = location.href;

export const switchEnv = url => {
  let ret = url;
  if (
    CURRENT_DOMAIN.includes("po2v.tb.zzzc.qihoo.net") ||
    CURRENT_DOMAIN.includes("10.174.224.174") ||
    CURRENT_DOMAIN.includes("quest.qihoo.ai") ||
    CURRENT_DOMAIN.includes("10.16.111.186")
  ) {
    ret = ret.replace(
      /http:\/\/[^/]+/gi,
      "http://p42250v.hulk.shbt.qihoo.net:8091"
    );
  }
  return ret;
};
