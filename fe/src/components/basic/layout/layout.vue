<template>
  <Layout class="main">
    <Layout>
      <!-- <Header class="header-con">
        <slot name="header"></slot>
      </Header> -->
      <Content class="content-wrapper">
        <slot></slot>
      </Content>
      <Footer>
        About
      </Footer>
    </Layout>
  </Layout>
</template>
<style scoped>
.ivu-layout-footer {
  padding: 22px 50px;
  background: #343741;
  color: #fff;
  text-align: center;
}
</style>
<script>
import { Layout, Content, Footer } from "iview";
import "./layout.less";
export default {
  name: "biLayout",
  components: { Layout, Content, Footer },
  data() {
    return {
      isCollapsed: false
    };
  }
};
</script>
