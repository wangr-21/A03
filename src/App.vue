<template>
  <a-layout style="min-height: 100vh">
    <a-layout-header style="display: flex; align-items: center; z-index: 1000">
      <div class="logo-container">
        <h1 class="app-title" @click="goToHome"><span class="logo-icon">📚</span> 智能备课助手</h1>
      </div>
    </a-layout-header>
    <a-layout>
      <a-layout-sider width="200">
        <a-menu
          mode="inline"
          style="height: 100%; border-right: 0"
          :selected-keys="[activeMenuKey]"
          class="custom-menu"
        >
          <a-menu-item v-for="item in menuItems" :key="item.key" class="menu-item">
            <template #icon>
              <item.icon />
            </template>
            <router-link :to="item.route" class="menu-link">{{ item.title }}</router-link>
          </a-menu-item>
        </a-menu>
      </a-layout-sider>
      <a-layout style="padding: 24px">
        <a-layout-content style="background: #fff; padding: 24px; margin: 0; min-height: 280px">
          <router-view />
        </a-layout-content>
      </a-layout>
    </a-layout>
  </a-layout>
</template>

<script setup lang="ts">
import { BookOutlined, DatabaseOutlined, BarChartOutlined } from '@ant-design/icons-vue';
import { ref, provide, watch, FunctionalComponent } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const router = useRouter();
// 创建响应式的活动菜单键值
const activeMenuKey = ref('');

// 提供给子组件使用的设置菜单项方法
const setActiveMenuItem = (key: string) => {
  activeMenuKey.value = key;
};

// 提供给子组件使用
provide('setActiveMenuItem', setActiveMenuItem);

// 添加返回首页的方法
const goToHome = () => {
  router.push('/');
  setActiveMenuItem(''); // 清除菜单选中项
};

// 监听路由变化，自动更新菜单状态
const route = useRoute();
watch(
  () => route.path,
  (newPath) => {
    // 根据路径设置活动菜单项
    if (newPath.includes('/workbench')) {
      setActiveMenuItem('1');
    } else if (newPath.includes('/resources')) {
      setActiveMenuItem('2');
    } else if (newPath.includes('/analysis')) {
      setActiveMenuItem('3');
    } else {
      setActiveMenuItem('');
    }
  },
  { immediate: true }
);

const menuItems = [
  {
    key: '1',
    icon: BookOutlined,
    title: '教师工作台',
    route: '/workbench',
  },
  {
    key: '2',
    icon: DatabaseOutlined,
    title: '资源中心',
    route: '/resources',
  },
  {
    key: '3',
    icon: BarChartOutlined,
    title: '数据分析',
    route: '/analysis',
  },
] as {
  key: string;
  icon: FunctionalComponent;
  title: string;
  route: string;
}[];
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.logo-container {
  display: flex;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.1);
  padding: 0 15px;
  border-radius: 4px;
  margin-right: 20px;
  position: relative;
  z-index: 1001;
}

.app-title {
  color: #fff;
  margin: 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  font-weight: 500;
  position: relative;
  padding: 6px 0;
  transition: all 0.3s;
}

.app-title:hover {
  color: #40a9ff; /* 鼠标悬停时使用Ant Design的主题蓝色 */
  text-shadow: 0 0 8px rgba(24, 144, 255, 0.5);
}

.app-title:after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: #40a9ff;
  transition: width 0.3s;
  z-index: 1002;
}

.app-title:hover:after {
  width: 100%;
}

.logo-icon {
  font-size: 20px;
  margin-right: 8px;
}

/* 侧边栏菜单自定义样式 */
.custom-menu .ant-menu-item {
  position: relative;
  overflow: visible;
}

.menu-link {
  position: relative;
  display: inline-block;
  width: 100%;
  transition: color 0.3s;
}

.menu-link:after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: #40a9ff;
  transition: width 0.3s;
  z-index: 10;
}

.ant-menu-item:hover .menu-link {
  color: #40a9ff !important;
  text-shadow: 0 0 8px rgba(24, 144, 255, 0.3);
}

.ant-menu-item:hover .menu-link:after {
  width: 100%;
}

/* 当菜单项被选中时保持下划线效果 */
.ant-menu-item-selected .menu-link:after {
  width: 100%;
}

/* 覆盖Ant Design默认选中样式 */
.custom-menu.ant-menu:not(.ant-menu-horizontal) .ant-menu-item-selected {
  background-color: rgba(24, 144, 255, 0.1);
}

.custom-menu.ant-menu-inline .ant-menu-item::after {
  border-right: 3px solid #40a9ff;
}
</style>
