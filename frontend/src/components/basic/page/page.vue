<template>
  <div class="pager">
    <div class="total">
      显示第1至 {{ page_length }}项结果，共 {{ data_total }}项
    </div>

    <page
      :total="data_total"
      show-elevator
      show-sizer
      :page-size-opts="[10]"
      @on-change="handleChange"
      @on-page-size-change="handleSizeChange"
    />
  </div>
</template>
<script>
import { Page } from "iview";
import "./index.less";
export default {
  name: "biPage",
  components: { Page },
  props: {
    data_total: {
      type: Number,
      default: 0
    },
    page_length: {
      type: Number,
      default: 1
    }
  },
  methods: {
    /**
     * 页码改变的回调，返回改变后的页码
     */
    handleChange(val) {
      this.$emit("change", val);
    },

    /**
     * 切换每页条数时的回调，返回切换后的每页条数
     */
    handleSizeChange(val) {
      this.$emit("sizeChange", val);
    }
  }
};
</script>
