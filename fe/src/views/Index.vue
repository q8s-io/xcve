<template>
  <bi-layout>
    <template v-slot:header>
      <Header></Header>
    </template>

    <template>
      <router-view />
    </template>
  </bi-layout>
</template>

<script>
import Header from "@components/business/header/index.vue";

export default {
  components: {
    Header
  },
  data() {
    return {};
  },
  beforeRouteEnter(to, from, next) {
    next();
  },
  methods: {}
};
</script>
