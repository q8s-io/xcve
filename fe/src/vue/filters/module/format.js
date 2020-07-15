import Utils from "@helper/utils.js";

export default (value, format = "yyyy-MM-dd hh:mm:ss") => {
  return Utils.formatTime(value, format);
};
