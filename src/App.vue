<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { RouterView } from 'vue-router'

// 响应式侧边栏控制
const sidebarCollapsed = ref(false);
const isMobile = ref(false);

const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value;
};

// 响应式设计 - 窗口大小检测
const handleResize = () => {
  isMobile.value = window.innerWidth < 768;
  // 在移动设备上自动折叠侧边栏
  if (isMobile.value) {
    sidebarCollapsed.value = true;
  } else {
    // 在桌面端默认展开侧边栏
    sidebarCollapsed.value = false;
  }
};

onMounted(() => {
  handleResize(); // 初始检查
  window.addEventListener('resize', handleResize);
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize);
});

// 模拟通知数据
const hasNotifications = ref(true);
</script>

<template>
  <div class="app-container" :class="{ 'sidebar-collapsed': sidebarCollapsed, 'mobile': isMobile }">
    <!-- 侧边栏 -->
    <div class="sidebar">
      <div class="logo-container">
        <img alt="Logo" class="logo" src="@/assets/logo.svg" />
        <span class="app-name" v-if="!sidebarCollapsed">智教通平台</span>
      </div>

      <!-- 菜单导航 -->
      <el-menu
        class="sidebar-menu"
        background-color="#7353E5"
        text-color="#ffffff"
        active-text-color="#ffffff"
        :default-active="$route.path"
        :collapse="sidebarCollapsed"
        router
      >
        <el-menu-item index="/" route="/">
          <el-icon><Grid /></el-icon>
          <template #title>启智学堂</template>
        </el-menu-item>
        <el-menu-item index="/workshop" route="/workshop">
          <el-icon><ChatDotRound /></el-icon>
          <template #title>智课工坊</template>
        </el-menu-item>
        <el-menu-item index="/lab" route="/lab">
          <el-icon><PictureFilled /></el-icon>
          <template #title>幻画实验室</template>
        </el-menu-item>
        <el-menu-item index="/lighthouse" route="/lighthouse">
          <el-icon><User /></el-icon>
          <template #title>学海灯塔</template>
        </el-menu-item>
        <el-menu-item index="/community" route="/community">
          <el-icon><PriceTag /></el-icon>
          <template #title>师韵星盟</template>
        </el-menu-item>
      </el-menu>

      <!-- 底部欢迎语 -->
      <div class="welcome-text" v-if="!sidebarCollapsed">
        <p>欢迎来到智教通平台！</p>
        <p class="sub-text">AI赋能教学，引领未来教育</p>
        <el-button type="primary" class="open-btn">现在开始！</el-button>
      </div>

      <!-- 折叠按钮 -->
      <div class="sidebar-collapse-btn" @click="toggleSidebar">
        <el-icon v-if="sidebarCollapsed"><ArrowRight /></el-icon>
        <el-icon v-else><ArrowLeft /></el-icon>
      </div>
    </div>

    <!-- 主内容区 -->
    <main class="main-content">
      <header class="header">
        <!-- 移动端菜单按钮 -->
        <div class="mobile-menu-toggle" v-if="isMobile" @click="toggleSidebar">
          <el-icon><Menu /></el-icon>
        </div>

        <!-- 面包屑 -->
        <div class="breadcrumb" v-if="!isMobile">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{ $route.meta.title || '当前页面' }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>

        <div class="right-tools">
          <el-badge is-dot :hidden="!hasNotifications">
            <el-icon class="tool-icon"><Bell /></el-icon>
          </el-badge>
          <el-icon class="tool-icon"><Setting /></el-icon>
          <div class="user-avatar">
            <img src="@/assets/avatar.svg" alt="用户头像" />
          </div>
        </div>
      </header>

      <!-- 路由内容视图 -->
      <div class="page-container">
        <RouterView v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </RouterView>
      </div>
    </main>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  width: 100%;
  overflow: hidden;
  font-family: 'PingFang SC', 'Helvetica Neue', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f5f7fa;
  color: #303133;
  margin: 0;
  padding: 0;
}

body {
  position: relative;
}

.app-container {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  margin: 0;
  padding: 0;
}

/* 侧边栏样式 */
.sidebar {
  width: 260px;
  background: linear-gradient(to bottom, #7353E5, #6B42E8);
  color: white;
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
  transition: all 0.3s ease;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  flex-shrink: 0;
  margin: 0;
  padding: 0;
}

/* 侧边栏折叠状态 */
.app-container.sidebar-collapsed .sidebar {
  width: 64px;
}

/* 移动设备样式 */
.app-container.mobile .sidebar {
  position: fixed;
  left: -260px;
  height: 100%;
}

.app-container.mobile.sidebar-collapsed .sidebar {
  left: 0;
  width: 230px;
}

@media (max-width: 768px) {
  .sidebar {
    width: 230px; /* 在较小屏幕上调整侧边栏宽度 */
  }
}

.logo-container {
  display: flex;
  align-items: center;
  padding: 1.25rem; /* 使用rem代替px */
  height: 64px;
}

.logo {
  width: 32px;
  height: 32px;
}

.app-name {
  font-size: 1.375rem; /* 使用rem代替px */
  font-weight: bold;
  margin-left: 0.625rem; /* 使用rem代替px */
  white-space: nowrap;
}

.welcome-text {
  margin-top: auto;
  padding: 1.25rem; /* 使用rem代替px */
  text-align: center;
}

.sub-text {
  font-size: 0.75rem; /* 使用rem代替px */
  margin-top: 0.3125rem; /* 使用rem代替px */
  opacity: 0.7;
}

.open-btn {
  width: 100%;
  margin-top: 0.9375rem; /* 使用rem代替px */
  background-color: #54D6FF;
  border: none;
}

/* 侧边栏折叠按钮 */
.sidebar-collapse-btn {
  position: absolute;
  right: -12px;
  top: 70px;
  width: 24px;
  height: 24px;
  background-color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.12);
  z-index: 2;
}

.sidebar-collapse-btn .el-icon {
  font-size: 12px;
  color: #909399;
}

/* 主内容区样式 */
.main-content {
  flex: 1;
  overflow-y: auto;
  background-color: #f5f7fa;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  position: relative;
  width: calc(100% - 260px); /* 桌面默认宽度 */
  height: 100%;
}

.app-container.sidebar-collapsed .main-content {
  width: calc(100% - 64px); /* 侧栏折叠时的宽度 */
}

.app-container.mobile .main-content {
  margin-left: 0;
  width: 100%; /* 移动端宽度占满 */
}

.header {
  height: 64px;
  background-color: white;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.5rem; /* 使用rem代替px */
  position: sticky;
  top: 0;
  z-index: 10;
}

.mobile-menu-toggle {
  display: none;
}

.app-container.mobile .mobile-menu-toggle {
  display: block;
  font-size: 1.5rem;
  cursor: pointer;
}

.breadcrumb {
  margin-right: auto;
}

.right-tools {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.tool-icon {
  font-size: 1.375rem; /* 使用rem代替px */
  color: #606266;
  cursor: pointer;
}

.user-avatar {
  width: 2.25rem; /* 使用rem代替px */
  height: 2.25rem; /* 使用rem代替px */
  border-radius: 50%;
  overflow: hidden;
  box-shadow: 0 0 0 2px rgba(115, 83, 229, 0.2);
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 页面容器 */
.page-container {
  padding: 1.5rem;
  flex: 1;
  overflow-x: hidden; /* 防止横向溢出 */
  width: 100%; /* 确保内容占满容器 */
  max-width: 1600px; /* 内容最大宽度 */
  margin: 0 auto; /* 居中显示 */
}

/* 页面过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 定制 Element Plus */
.el-menu {
  border-right: none !important;
}

.el-menu--collapse {
  width: 64px;
}

.el-menu-item.is-active {
  background-color: rgba(255, 255, 255, 0.15) !important;
}

.el-menu-item:hover {
  background-color: rgba(255, 255, 255, 0.1) !important;
}

/* 桌面端响应式调整 */
@media (min-width: 1600px) {
  .page-container {
    max-width: 1600px;
  }
}

/* 平板端响应式调整 */
@media (min-width: 768px) and (max-width: 1199px) {
  .page-container {
    padding: 1rem;
  }
}

/* 大屏幕适配 */
@media (min-width: 1920px) {
  .page-container {
    max-width: 1800px;
  }
}

/* 适配各种页面内容 */
.el-card {
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.el-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* 确保元素Plus组件在深色背景上的可见性 */
.el-menu .el-icon,
.sidebar .el-menu-item {
  color: white !important;
}

.sidebar-menu .el-menu-item i {
  color: white !important;
}

.el-menu--collapse .el-menu-item span {
  display: none;
}

/* 修复各种组件显示问题 */
.el-table {
  --el-table-header-bg-color: #f5f7fa;
  --el-table-row-hover-bg-color: rgba(115, 83, 229, 0.05);
}

.el-pagination {
  margin-top: 16px;
  justify-content: flex-end;
}

.el-progress-bar__inner {
  transition: width 0.6s ease;
}

.el-input__wrapper {
  box-shadow: 0 0 0 1px #dcdfe6 inset;
}

.el-input__wrapper:hover {
  box-shadow: 0 0 0 1px #7353E5 inset;
}

.el-input__wrapper.is-focus {
  box-shadow: 0 0 0 1px #7353E5 inset !important;
}

.el-button--primary {
  --el-button-bg-color: #7353E5;
  --el-button-border-color: #7353E5;
  --el-button-hover-bg-color: #8A6AFF;
  --el-button-hover-border-color: #8A6AFF;
  --el-button-active-bg-color: #6B42E8;
  --el-button-active-border-color: #6B42E8;
}
</style>
