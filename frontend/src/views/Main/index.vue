<template>
  <div class="index-wrap">
    <div class="icon-wrap">
      <i class="icon"></i>
      <bi-auto-complete
        :placeholder="placeholder"
        clearable
        style="width:530px;"
        @keyup.enter.native="onSearch"
        @on-search="handleSearch"
        @on-select="onSelect"
        v-model="keyword"
        class="ipt"
        @on-focus="onFocus"
      >
      <i-option v-for="(item,index) in dataList" :value="JSON.stringify(item)" :key="index"><span :style="`color: ${conf[item.class].color };`">{{item.name}}</span></i-option>
        <bi-icon type="md-search" slot="prefix" />
      </bi-auto-complete>
      <!-- <p class="top-title">Top Searches</p>
      <div class="top-list">
        <ul>
          <template v-for="(item,index) in entities">
            <li :key="index" v-if="index<5" @click="onTopClick(item)"><i :style="`background: ${conf[item.class].color }`"></i>{{item.name}}</li>
          </template>
        </ul>
      </div> -->
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
      placeholder: "",
      type: "",
      dataList: [],
      entities:[]
    };
  },
  computed: {},
  methods: {
    async init() {
      await this.getConf();
      await this.getRandomData();
    },
    async getConf() {
      let ret = await getConf();
      if (ret && ret.graph) {
        this.conf = ret.graph;
      }
    },
    onSearch() {
      if(this.keyword === '') {
        this.keyword = this.placeholder;
      }
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
      setTimeout(() => {
        let ret = JSON.parse(item);
        this.keyword = ret.name;
        this.type = ret.class;
        this.$forceUpdate();
        this.onSearch();
      }, 0);
    },
    onTopClick(item) {
      this.keyword = item.name;
      this.type = item.class;
      this.onSearch();
    },
    async getRandomData() {
      let ret = await getRandom();
      this.entities = ret;
      let index = Math.floor(Math.random() * this.entities.length);
      this.placeholder = this.entities[index].name;
      this.type = this.entities[index].class;
      console.log(this.entities);
    },
    onFocus() {
      if(this.keyword === '') {
        this.dataList = this.entities;
      }
    }
  },
  beforeMount() {
    this.init();
  },
  mounted() {}
};
</script>
