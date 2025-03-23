<template>
  <div class="home-container">
    <div class="welcome-section">
      <h1 class="welcome-title">欢迎使用智能备课助手</h1>
      <div class="welcome-divider"></div>
      <p class="welcome-subtitle">高效备课，智能辅助，提升教学质量</p>
    </div>

    <el-row :gutter="24" class="quick-links">
      <el-col v-for="link in quickLinks" :key="link.menuKey" :xs="24" :sm="12" :md="8">
        <el-card shadow="hover" class="link-card" @click="navigateTo(link.route, link.menuKey)">
          <div class="card-content">
            <el-icon :size="36" class="card-icon">
              <component :is="link.icon" />
            </el-icon>
            <h3>{{ link.title }}</h3>
            <p>{{ link.description }}</p>
          </div>
        </el-card>
      </el-col>
    </el-row>
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

const quickLinks = [
  {
    title: '教师工作台',
    description: '开始您的备课工作',
    route: '/workbench',
    menuKey: '1',
    icon: 'Reading',
  },
  {
    title: '资源中心',
    description: '浏览教学资源库',
    route: '/resources',
    menuKey: '2',
    icon: 'Files',
  },
  {
    title: '数据分析',
    description: '查看教学数据分析',
    route: '/analysis',
    menuKey: '3',
    icon: 'DataAnalysis',
  },
] as {
  title: string;
  description: string;
  route: string;
  menuKey: string;
  icon: string;
}[];
</script>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
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
  color: #409eff; /* Element Plus 主题蓝色 */
  margin-bottom: 1rem;
  letter-spacing: 1px;
}

.welcome-divider {
  height: 3px;
  width: 80px;
  background: linear-gradient(to right, #409eff, #79bbff);
  margin: 0 auto 1.5rem;
  border-radius: 3px;
}

.welcome-subtitle {
  font-size: 1.1rem;
  color: #606266; /* Element Plus 次要文本颜色 */
  margin-bottom: 1rem;
  font-weight: 300;
}

.quick-links {
  width: 100%;
}

.link-card {
  height: 100%;
  cursor: pointer;
  transition: transform 0.3s;
}

.link-card:hover {
  transform: translateY(-5px);
}

.card-content {
  display: flex;
  flex-direction: column;
  height: 180px;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 1rem;
}

.card-icon {
  margin-bottom: 16px;
  color: #409eff;
}

h3 {
  margin-bottom: 0.8rem;
  color: #409eff;
  font-size: 1.25rem;
}

p {
  margin: 0;
  color: #606266;
  font-size: 0.95rem;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .card-content {
    height: auto;
    padding: 1.5rem 1rem;
  }

  .welcome-title {
    font-size: 2rem;
  }
}
</style>
