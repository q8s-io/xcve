<template>
  <div class="step-box" ref="box" :style="{ backgroundSize }">
    <template v-for="(item, index) of list">
      <div :key="item" class="step-item">
        <div class="icon-posi">
          <data-svg
            v-if="index === 0"
            width="20"
            height="20"
            fill="#2d8cf0"
          ></data-svg>
          <success-svg
            v-if="index === 1"
            width="20"
            height="20"
            :fill="current === 1 ? '#336699' : '#2d8cf0'"
          ></success-svg>
        </div>
        <slot
          ><p class="step-p">{{ item }}</p></slot
        >
      </div>
    </template>
  </div>
</template>
<style>
.step-box {
  height: 300px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  margin: 0 15px;
  background: linear-gradient(to bottom, #1296db, #1296db),
    linear-gradient(to right, white 49%, #4176ab 0, #4176ab 51%, white 0);
  background-size: 2% 0%, 100% 100%;
  background-position: 50% 0, 0 0;
  background-repeat: no-repeat;
  transition: all 0.5s ease-out;
}
.step-item {
  background: white;
  padding: 5px 0;
}
.step-p {
  text-align: center;
}
.link {
  position: absolute;
  width: 2px;
  height: 100px;
  background: #336699;
}
.icon-posi {
  text-align: center;
}
</style>
<script>
import DataSvg from "@/assets/svg/data.svg";
import SuccessSvg from "@/assets/svg/success.svg";
const linkWidth = 2;
export default {
  name: "MyStep",
  components: {
    DataSvg,
    SuccessSvg
  },
  data() {
    return {
      list: ["选择数据来源", "完成"],
      links: []
    };
  },
  watch: {},
  props: {
    current: {
      type: Number,
      default: 1
    }
  },
  mounted() {
    this.$nextTick(() => {
      const boxs = Array.prototype.slice.call(
        document.getElementsByClassName("step-box")
      );
      boxs.forEach(box => {
        const items = box.getElementsByClassName("step-item");
        const item1 = items[0];
        const item2 = items[1];
        const { offsetHeight: h1, offsetTop: top1, offsetWidth: w1 } = item1;
        const { offsetHeight: h2, offsetTop: top2 } = item2;
        console.log(h1, top1, h2, top2, w1);
        this.links.push({ ...this.calc(h1, top1, h2, top2, w1), index: 0 });
      });
    });
  },
  methods: {
    calc(h1, top1, h2, top2, width) {
      const gap = 5;
      return {
        left: width - linkWidth / 2,
        top: top1 + h1 + gap,
        height: top2 - top1 - h1 - 2 * gap
      };
    }
  },
  computed: {
    backgroundSize() {
      const height = ((this.current - 1) / (this.list.length - 1)) * 100;
      return `2% ${height}%, 100% 100%`;
    }
  }
};
</script>
