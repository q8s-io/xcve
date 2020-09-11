/*引入封装组件*/
import Layout from "@components/basic/layout/index.js";
import Title from "@components/business/title";
import Page from "@components/basic/page/index.js";

import {
  Button,
  ButtonGroup,
  Menu,
  MenuItem,
  Submenu,
  Table,
  Divider,
  Icon,
  Modal,
  Input,
  AutoComplete,
  Form,
  FormItem,
  Row,
  Col,
  Select,
  Option,
  RadioGroup,
  Radio,
  CheckboxGroup,
  Checkbox,
  Poptip,
  Tooltip,
  Tabs,
  TabPane,
  List,
  Breadcrumb,
  BreadcrumbItem,
  DatePicker,
  Message,
  Card,
  Spin,
  Cascader,
  Notice,
  Upload,
  Progress,
  Steps,
  Step,
  Scroll,
  BackTop
} from "iview";

const components = {
  Button,
  ButtonGroup,
  Layout,
  Menu,
  MenuItem,
  Submenu,
  Table,
  Divider,
  Page,
  Icon,
  Modal,
  Input,
  AutoComplete,
  Form,
  FormItem,
  Row,
  Col,
  Select,
  RadioGroup,
  Radio,
  CheckboxGroup,
  Checkbox,
  Poptip,
  Tooltip,
  Tabs,
  TabPane,
  Title,
  List,
  ListItem: List.Item,
  ListItemMeta: List.Item.Meta,
  Breadcrumb,
  BreadcrumbItem,
  DatePicker,
  Card,
  Spin,
  Cascader,
  Notice,
  Upload,
  Progress,
  Steps,
  Step,
  Scroll,
  BackTop
};

const install = function(Vue) {
  Object.keys(components).forEach(key => {
    Vue.component(`bi${key}`, components[key]);
  });

  Vue.component(`iOption`, Option);

  Vue.prototype.$Modal = Modal;
  Vue.prototype.$Message = Message;
  Vue.prototype.$Notice = Notice;
  Vue.prototype.$Spin = Spin;
};

// auto install
if (typeof window !== "undefined" && window.Vue) {
  install(window.Vue);
}

export default {
  install
};
