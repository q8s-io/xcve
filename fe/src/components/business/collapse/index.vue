<template>
  <div
    :class="{
      'common-collapse': true,
      closed: isCollapsed,
      left: this.position == 'left'
    }"
  >
    <div class="content">
      <slot name="content"></slot>
    </div>
    <div class="icons" @click="onCollapse">
      <template v-if="position == 'right'">
        <bi-icon type="ios-arrow-back" v-if="!isCollapsed" size="20" />
        <bi-icon type="ios-arrow-forward" v-if="isCollapsed" size="20" />
      </template>
      <template v-if="position == 'left'">
        <bi-icon type="ios-arrow-back" v-if="isCollapsed" size="20" />
        <bi-icon type="ios-arrow-forward" v-if="!isCollapsed" size="20" />
      </template>
    </div>
  </div>
</template>

<script>
import "./index.less";
export default {
  name: "Collapse",
  props: {
    position: {
      type: String,
      default: "right"
    }
  },
  data() {
    return {
      isCollapsed: false
    };
  },
  computed: {},
  methods: {
    onCollapse() {
      this.isCollapsed = !this.isCollapsed;
    }
  }
};
</script>
