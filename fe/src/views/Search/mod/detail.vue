<template>
  <div class="detail-mod">
    <div class="tabs-mod">
      <bi-tabs type="card">
        <bi-tab-pane label="原始文档">
          <div class="file-detail">
            <iframe
              ref="iframe"
              class="file-container"
              :src="detail.url"
              type="application/pdf"
            ></iframe>
          </div>
        </bi-tab-pane>
        <bi-tab-pane label="解析文本">
          <div class="html-detail">
            <div class="detail-wrap" v-html="detail.all"></div>
          </div>
        </bi-tab-pane>
        <!-- <bi-tab-pane label="可视化图谱">标签三的内容</bi-tab-pane> -->
      </bi-tabs>
    </div>
    <div class="searchs-mod">
      <!-- <h3>搜索/标签</h3>
      <div class="form-mod flex">
        <bi-input
          placeholder="有多少清华大学毕业的员工"
          style="width:75%;"
          clearable
        />
        <bi-button type="primary" class="btn">
          搜索
        </bi-button>
      </div> -->
      <bi-card class="filter-mod" dis-hover>
        <!-- :key="index" v-for="(item, index) in detail.properties" -->
        <template v-for="(detail, index) in detail.properties">
          <div
            class="type-mod"
            :key="`${index}-${key}`"
            v-for="(item, key) in detail"
          >
            <div class="type-name">{{ properties[index] }}</div>
            <div class="type-item">
              <span>{{ item }}</span>
            </div>
          </div>
        </template>
      </bi-card>
      <!-- <bi-card class="simlar-wrap"></bi-card> -->
    </div>
  </div>
</template>
<style lang="less"></style>
<script>
import "./index.less";
export default {
  data() {
    return {};
  },
  props: {
    detail: {
      type: Object
    },
    properties: {
      type: Object
    }
  },
  components: {},
  computed: {
    detailHtml() {
      //return `<p>${this.detail.replace(/\n/gi, "</p><p>")}</p>`;
      return ``;
    }
  },
  methods: {}
};
</script>
