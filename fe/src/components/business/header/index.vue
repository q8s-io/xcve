<template>
  <div class="header">
    <a @click="handleChange" type="text" class="logo-name">
      <!-- <bi-icon type="md-menu" :size="26" /> -->
    </a>

    <div class="right">
      <!-- <bi-icon type="md-search" :size="20" /> -->
      <!-- <bi-icon type="ios-notifications-outline" :size="20" /> -->

      <!-- <div class="user">
        <bi-icon type="logo-octocat" :size="20" />
        <span class="name">用户</span>
      </div> -->
    </div>
  </div>
</template>
<script>
import "./index.less";
export default {
  name: "biHeader",
  methods: {
    handleChange() {}
  }
};
</script>
