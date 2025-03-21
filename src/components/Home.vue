<template>
  <div class="home-container">
    <div class="welcome-section">
      <h1 class="welcome-title">欢迎使用智能备课助手</h1>
      <div class="welcome-divider"></div>
      <p class="welcome-subtitle">高效备课，智能辅助，提升教学质量</p>
    </div>

    <div class="quick-links">
      <div class="link-card" @click="navigateTo('/workbench', '1')">
        <div class="card-content">
          <h3>教师工作台</h3>
          <p>开始您的备课工作</p>
        </div>
      </div>

      <div class="link-card" @click="navigateTo('/resources', '2')">
        <div class="card-content">
          <h3>资源中心</h3>
          <p>浏览教学资源库</p>
        </div>
      </div>

      <div class="link-card" @click="navigateTo('/analysis', '3')">
        <div class="card-content">
          <h3>数据分析</h3>
          <p>查看教学数据分析</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { inject } from 'vue';

const router = useRouter();
// 注入在App.vue中提供的设置活动菜单项的方法
const setActiveMenuItem = inject('setActiveMenuItem') as (menuKey: string) => void;

const navigateTo = (path: string, menuKey: string) => {
  // 更新侧边栏选中状态
  if (setActiveMenuItem) {
    setActiveMenuItem(menuKey);
  }
  // 导航到相应页面
  router.push(path);
};
</script>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
}

.welcome-section {
  text-align: center;
  margin-bottom: 3rem;
  width: 100%;
  max-width: 800px;
}

.welcome-title {
  font-size: 2.5rem;
  font-weight: 600;
  color: #1890ff; /* Ant Design 主题蓝色 */
  margin-bottom: 1rem;
  letter-spacing: 1px;
}

.welcome-divider {
  height: 3px;
  width: 80px;
  background: linear-gradient(to right, #1890ff, #40a9ff);
  margin: 0 auto 1.5rem;
  border-radius: 3px;
}

.welcome-subtitle {
  font-size: 1.1rem;
  color: #666;
  margin-bottom: 1rem;
  font-weight: 300;
}

.quick-links {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  justify-content: center;
  max-width: 1200px;
}

.link-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 280px;
  height: 180px;
  text-decoration: none;
  color: inherit;
  transition: transform 0.3s, box-shadow 0.3s;
  overflow: hidden;
  cursor: pointer;
}

.link-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.card-content {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  height: 100%;
  justify-content: center;
  align-items: center;
  text-align: center;
}

h3 {
  margin-bottom: 0.5rem;
  color: #3498db;
}

p {
  margin: 0;
  color: #666;
}
</style>
