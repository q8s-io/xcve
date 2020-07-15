<template>
  <div class="index-wrap">
    <div class="icon-wrap">
      <i class="icon"></i>
      <bi-auto-complete
        placeholder="Image/CVE"
        clearable
        style="width:530px;"
        @keyup.enter.native="onSearch"
        @on-search="handleSearch"
        @on-select="onSelect"
        :data="dataList"
        v-model="keyword"
        class="ipt"
      >
        <bi-icon type="md-search" slot="prefix" />
      </bi-auto-complete>

      <bi-button type="primary" class="btn" @click="onSearch">
        Search
      </bi-button>
    </div>
  </div>
</template>

<script>
import "./index.less";
import { getSuggest } from "@api/search.js";
export default {
  name: "search-index",
  components: {},
  data() {
    return {
      keyword: "CVE-1999-0130",
      dataList: []
    };
  },
  computed: {},
  methods: {
    async init() {
      this.getDetailData();
    },
    onSearch() {
      this.$router.push({
        path: "/search",
        query: {
          keyword: this.keyword
        }
      });
    },
    handleSearch(value) {
      getSuggest({
        prefix: value
      }).then(ret => {
        this.dataList = ret;
      });
    },
    onSelect(value) {
      this.keyword = value;
      this.onSearch();
    }
  },
  beforeMount() {
    this.init();
  },
  mounted() {}
};
</script>
