const CURRENT_DOMAIN = location.href;

export const switchEnv = url => {
  let ret = url;
  if (
    CURRENT_DOMAIN.includes("q8s.io")
  ) {
    ret = ret.replace(
      /http:\/\/[^/]+/gi,
      "http://q8s.io"
    );
  }
  return ret;
};
