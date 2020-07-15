<template>
  <div class="search-wrap">
    <div class="banner">
      <div class="top">
        <router-link to="/" class="search-icon"> </router-link>
        <bi-auto-complete
          placeholder="Image/CVE"
          clearable
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
    <div class="content">
      <div class="maps" ref="maps">
        <div class="graph">
          <h3>Relation</h3>
          <h4>{{ entryName }}</h4>
          <div id="graphDom" ref="graph"></div>
        </div>
      </div>
      <div class="info">
        <h3>{{ entryName }}</h3>
        <p class="desc"></p>
        <div class="basic-info">
          <bi-table
            :columns="basicInfo.columns"
            :data="basicInfo.data"
          ></bi-table>
        </div>
        <div class="relation">
          <bi-table
            :columns="relationInfo.columns"
            :data="relationInfo.data"
          ></bi-table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import "./index.less";
// import G6 from "@antv/g6";
import { getSuggest, getDetail, getConf } from "@api/search.js";
export default {
  name: "search-index",
  components: {},
  data() {
    return {
      keyword: "",
      dataList: [],
      basicInfo: {
        columns: [
          {
            title: "Basic Information",
            key: "key"
          },
          {
            title: " ",
            key: "val"
          }
        ],
        data: []
      },
      relationInfo: {
        columns: [
          {
            title: "Relations",
            key: "key"
          },
          {
            title: " ",
            key: "val"
          }
        ],
        data: []
      },
      graphData: {
        nodes: [],
        edges: []
      },
      detail: {},
      conf: {}
    };
  },
  computed: {},
  methods: {
    async init() {
      await this.getConf();
      await this.getDetailData();
      this.initGraph();
    },
    async getConf() {
      let ret = await getConf();
      if (ret && ret.graph) {
        this.conf = ret.graph;
      }
    },
    drawGraph() {
      let size = 50;
      this.$refs.graph.innerHTML = "";
      const graph = new G6.Graph({
        container: "graphDom",
        width: this.$refs.maps.offsetWidth - 50,
        height: this.$refs.maps.offsetHeight - 150,
        fitCenter: true,
        // 节点默认配置
        defaultNode: {
          size: size,
          labelCfg: {
            style: {
              fill: "#fff"
            }
          }
        },
        // 边默认配置
        defaultEdge: {
          labelCfg: {
            autoRotate: true
          }
        },
        // 节点在各状态下的样式
        nodeStateStyles: {
          // hover 状态为 true 时的样式
          hover: {
            fill: "lightsteelblue"
          },
          // click 状态为 true 时的样式
          click: {
            stroke: "#999",
            lineWidth: 3
          }
        },
        // 边在各状态下的样式
        edgeStateStyles: {
          // click 状态为 true 时的样式
          click: {
            stroke: "steelblue"
          }
        },
        // 布局
        layout: {
          type: "force",
          linkDistance: 150,
          preventOverlap: true,
          nodeStrength: -100,
          edgeStrength: 0.1
        }
        // 内置交互
        // modes: {
        //     default: ['drag-canvas', 'zoom-canvas'],
        // },
      });

      const main = async () => {
        // const response = await fetch(
        //     'https://gw.alipayobjects.com/os/basement_prod/6cae02ab-4c29-44b2-b1fd-4005688febcb.json',
        // );
        // const remoteData = await response.json();
        const remoteData = this.graphData;
        const nodes = remoteData.nodes;
        const edges = remoteData.edges;
        nodes.forEach(node => {
          if (!node.style) {
            node.style = {};
          }
          node.style.lineWidth = 1;
          node.style.stroke = "#EB2728";
          node.style.fill = "#F16667";

          node.labelCfg = {
            style: {
              position: "left",
              fill: "#000",
              fontSize: 13
            }
          };
          node.type = "circle";
          node.size = size;
          node.style.stroke = "#C0A378";
          node.style.fill = this.conf[node.class].color || "#D9C8AE";
        });
        edges.forEach(edge => {
          if (!edge.style) {
            edge.style = {};
          }
          edge.style.lineWidth = edge.weight;
          //console.log(`edge.weight--${edge.weight}`);
          //edge.style.opacity = 0.6;
          edge.style.stroke = "#C4C9D0";
        });

        graph.data(remoteData);
        graph.render();

        // 监听鼠标进入节点
        graph.on("node:mouseenter", e => {
          const nodeItem = e.item;
          // 设置目标节点的 hover 状态 为 true
          graph.setItemState(nodeItem, "hover", true);
        });
        // 监听鼠标离开节点
        graph.on("node:mouseleave", e => {
          const nodeItem = e.item;
          // 设置目标节点的 hover 状态 false
          graph.setItemState(nodeItem, "hover", false);
        });
        // 监听鼠标点击节点
        graph.on("node:click", e => {
          // 先将所有当前有 click 状态的节点的 click 状态置为 false
          const clickNodes = graph.findAllByState("node", "click");
          clickNodes.forEach(cn => {
            graph.setItemState(cn, "click", false);
          });
          const nodeItem = e.item;
          // 设置目标节点的 click 状态 为 true
          graph.setItemState(nodeItem, "click", true);
        });
        // 监听鼠标点击节点
        graph.on("edge:click", e => {
          // 先将所有当前有 click 状态的边的 click 状态置为 false
          const clickEdges = graph.findAllByState("edge", "click");
          clickEdges.forEach(ce => {
            graph.setItemState(ce, "click", false);
          });
          const edgeItem = e.item;
          // 设置目标边的 click 状态 为 true
          graph.setItemState(edgeItem, "click", true);
        });

        const forceLayout = graph.get("layoutController").layoutMethod;

        graph.on("node:dragstart", function(e) {
          graph.layout();
          refreshDragedNodePosition(e);
        });
        graph.on("node:drag", function(e) {
          forceLayout.execute();
          refreshDragedNodePosition(e);
        });
        graph.on("node:dragend", function(e) {
          e.item.get("model").fx = null;
          e.item.get("model").fy = null;
        });
      };
      main();

      function refreshDragedNodePosition(e) {
        const model = e.item.get("model");
        model.fx = e.x;
        model.fy = e.y;
      }
    },
    initGraph() {
      this.$nextTick(() => {
        document.querySelector("#graphDom");
        this.drawGraph();
      });
    },
    onSearch() {
      this.entryName = this.keyword;
      //console.log(this.entryName);
      this.init();
      this.drawGraph();
      this.$forceUpdate();
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
    },
    /**
     * 计算N个点均匀排列成圆的各个点坐标
     * @param nodeSize 参与排列成圆的元素个数
     * @param center 圆的中心点坐标 {x:, y:}
     * @param radius 圆的半径
     * @return 各个元素的坐标：[{x:, y:}, {x:, y:}, ...]
     */
    calcCircularLayout(nodeSize, center, radius) {
      var i,
        _i,
        _layouts = [];
      for (i = _i = 0; _i < nodeSize; i = ++_i) {
        var x = center.x + radius * Math.sin((2 * Math.PI * i) / nodeSize),
          y = center.y + radius * Math.cos((2 * Math.PI * i) / nodeSize);

        _layouts.push({ x: x, y: y });
      }

      return _layouts;
    },
    async getDetailData() {
      let ret = await getDetail({
        cve_id: this.keyword
      });
      this.detail = ret;
      this.basicInfo.data = [];
      if (ret && ret[this.keyword]) {
        for (let key in ret[this.keyword].cve) {
          key &&
            this.basicInfo.data.push({
              key: key,
              val: ret[this.keyword].cve[key]
            });
        }

        this.relationInfo.data = [];
        if (ret[this.keyword].counts) {
          for (let key in ret[this.keyword].counts) {
            key &&
              this.relationInfo.data.push({
                key: Object.keys(ret[this.keyword].counts[key])[0],
                val: Object.values(ret[this.keyword].counts[key])[0]
              });
          }
        }
        this.graphData = ret[this.keyword].relations;
        if (this.graphData.nodes) {
          let points = this.calcCircularLayout(
            this.graphData.nodes.length - 1,
            {
              x: 350,
              y: 400
            },
            200
          );
          this.graphData.nodes.map((item, index) => {
            if (index === 0) {
              item.x = 350;
              item.y = 400;
            } else {
              item.x = points[index - 1].x;
              item.y = points[index - 1].y;
            }
          });

          this.graphData.edges.map((item, index) => {
            item.source = `${item.source}`;
            item.target = `${item.target}`;
            item.weight = 2;
          });
        }
        console.log(JSON.stringify(this.graphData), "====>");
      }
    }
  },
  beforeMount() {
    this.keyword = this.$route.query.keyword;
    this.entryName = this.keyword;
  },
  mounted() {
    this.init();
  }
};
</script>
