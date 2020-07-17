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
        v-model="keyword"
        class="ipt"
      >
      <i-option v-for="(item,index) in dataList" :value="JSON.stringify(item)" :key="index">{{ item.name }}(<span :style="`color: ${conf[item.class].color };font-weight:bold;`">{{item.class}}</span>)</i-option>
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
import { getSuggest, getRandom,getConf } from "@api/search.js";
export default {
  name: "search-index",
  components: {},
  data() {
    return {
      keyword: "",
      type: "",
      dataList: [],
      entities:[]
    };
  },
  computed: {},
  methods: {
    async init() {
      this.getRandomData();
      this.getConf();
    },
    async getConf() {
      let ret = await getConf();
      if (ret && ret.graph) {
        this.conf = ret.graph;
      }
    },
    onSearch() {
      this.$router.push({
        path: "/s",
        query: {
          keyword: this.keyword,
          type: this.type
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
    onSelect(item) {
      let ret = JSON.parse(item);
      this.keyword = ret.name;
      this.type = ret.class;
      this.onSearch();
    },
    async getRandomData() {
      let ret = await getRandom();
      this.entities = ret;
      let index = Math.floor(Math.random() * this.entities.length);
      this.keyword = this.entities[index].name;
      this.type = this.entities[index].class;
      console.log(this.entities);
    }
  },
  beforeMount() {
    this.init();
  },
  mounted() {}
};
</script>
