<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
import "@/assets/css/global.less";
/*引入对基础组件的样式改写*/
import "@components/basic/index.less";

export default {
  components: {}
};
</script>

<style lang="less">
#app {
  height: 100vh;
}
</style>
