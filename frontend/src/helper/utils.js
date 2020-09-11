/**
 * 正则验证规则
 * @type {object}
 */
const regex = {
  // 邮箱
  email: /^[a-zA-Z0-9_\-|\\.]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/,
  // url
  url: /^(?:(?:(?:https?|ftp):)?\/\/)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})).?)(?::\d{2,5})?(?:[/?#]\S*)?$/i,
  // 手机号码
  mobile: /^1\d{10}$/,
  // 邮编
  postal: /^[a-zA-Z0-9 ]{3,12}$/g,
  // 银行卡号
  card: /^[\d]{16,19}$/
};

const formatTime = (d, format = "yyyy-MM-dd hh:mm:ss") => {
  var reg = {
    y: d.getFullYear(),
    M: d.getMonth() + 1,
    d: d.getDate(),
    h: d.getHours(),
    m: d.getMinutes(),
    s: d.getSeconds()
  };

  Object.keys(reg).forEach(key => {
    format = format.replace(new RegExp(key + "+"), a => {
      return ("0000" + reg[key]).slice(0 - a.length);
    });
  });
  return format;
};

const dateToUnixtime = date => {
  if (date) {
    const dateTime = new Date(date).getTime();
    const timestamp = Math.floor(dateTime / 1000);

    return timestamp;
  }

  return "";
};

const unixtimeToDate = unixtime => {
  if (unixtime) {
    const unixTimestamp = new Date(unixtime * 1000);
    return unixTimestamp.toLocaleString().replace(/\//g, ".");
  }

  return "";
};

export default {
  regex,
  formatTime,
  unixtimeToDate,
  dateToUnixtime
};
