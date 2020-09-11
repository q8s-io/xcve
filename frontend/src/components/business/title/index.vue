<template>
  <div class="bi-title">
    <div class="left-part">
      <div class="name">{{ title }}</div>
      <bi-icon
        class="g-tips-icon-32"
        v-if="tipsIcon"
        type="ios-alert-outline"
        size="14"
      />
    </div>

    <div class="right-part"><slot></slot></div>
  </div>
</template>

<script>
import "./index.less";
export default {
  name: "bi-title",
  data() {
    return {};
  },
  props: ["title", "tipsIcon", "tipsContent"]
};
</script>
