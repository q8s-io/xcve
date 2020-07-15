export default {
  /**
   * 获取数据列表
   */
  getList(state, { data = {} }) {
    state.listData = data;
  }
};
