<template>
  <el-container style="min-height: 100vh">
    <el-header style="display: flex; align-items: center; z-index: 1000">
      <div class="logo-container">
        <h1 class="app-title" @click="goToHome"><span class="logo-icon">📚</span> 智能备课助手</h1>
      </div>
    </el-header>
    <el-container>
      <el-aside width="200px">
        <el-menu mode="vertical" :default-active="activeMenuKey" class="custom-menu" router>
          <el-menu-item v-for="item in menuItems" :key="item.key" :index="item.route">
            <el-icon>
              <component :is="item.icon" />
            </el-icon>
            <span>{{ item.title }}</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-main style="padding: 24px">
          <div class="content-box">
            <router-view />
          </div>
        </el-main>
      </el-container>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { ref, provide, watch, DefineComponent } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { Reading, Files, DataAnalysis } from '@element-plus/icons-vue';

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
    icon: Reading,
    title: '教师工作台',
    route: '/workbench',
  },
  {
    key: '2',
    icon: Files,
    title: '资源中心',
    route: '/resources',
  },
  {
    key: '3',
    icon: DataAnalysis,
    title: '数据分析',
    route: '/analysis',
  },
] as {
  key: string;
  icon: DefineComponent;
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
  font-weight: 350;
  position: relative;
  padding: 6px 0;
  transition: all 0.3s;
}

.app-title:hover {
  color: #40a9ff;
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

.content-box {
  background: #fff;
  padding: 24px;
  margin: 0;
  min-height: 280px;
}

.el-header {
  background-color: #001529;
  padding: 0 20px;
}

.el-aside {
  border-right: 1px solid #e6e6e6;
}

.el-menu {
  border-right: none;
}
</style>
