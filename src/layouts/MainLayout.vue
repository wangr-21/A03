<script setup lang="ts">
import { defineAsyncComponent } from 'vue';
import { useResponsive } from '@/hooks/useResponsive';

const AppSidebar = defineAsyncComponent(() => import('@/components/layout/AppSidebar.vue'));
const AppHeader = defineAsyncComponent(() => import('@/components/layout/AppHeader.vue'));

const { sidebarCollapsed, isMobile, toggleSidebar } = useResponsive();


</script>

<template>
  <div class="app-container" :class="{ 'sidebar-collapsed': sidebarCollapsed, mobile: isMobile }">
    <AppSidebar
      :collapsed="sidebarCollapsed"
      :is-mobile="isMobile"
      @toggle-sidebar="toggleSidebar"
    />

    <main class="main-content">
      <AppHeader :is-mobile="isMobile" @toggle-sidebar="toggleSidebar" />

      <div class="page-container">
        <slot></slot>
      </div>
    </main>
  </div>
</template>

<style scoped>
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

/* 侧边栏折叠状态 */
.app-container.sidebar-collapsed :deep(.sidebar) {
  width: 64px;
}

/* 移动设备样式 */
.app-container.mobile :deep(.sidebar) {
  position: fixed;
  left: -260px;
  height: 100%;
}

.app-container.mobile.sidebar-collapsed :deep(.sidebar) {
  left: 0;
  width: 230px;
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

/* 页面容器 */
.page-container {
  padding: 1.5rem;
  flex: 1;
  overflow-x: hidden; /* 防止横向溢出 */
  width: 100%; /* 确保内容占满容器 */
  max-width: 1600px; /* 内容最大宽度 */
  margin: 0 auto; /* 居中显示 */
}

/* 响应式调整 */
@media (max-width: 768px) {
  :deep(.sidebar) {
    width: 230px; /* 在较小屏幕上调整侧边栏宽度 */
  }
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
</style>
