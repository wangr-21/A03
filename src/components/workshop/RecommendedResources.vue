<script setup lang="ts">
import { ref } from 'vue';
import * as avatars from '@/assets/avatars';

interface RecommendedResource {
  title: string;
  author: string;
  content: string;
  date: string;
  views: number;
  stars: number;
  avatar: string;
}

// 推荐资源数据
const resources = ref<RecommendedResource[]>([
  {
    title: '如何让数学课更有趣',
    author: '李明 · 特级教师',
    content: '分享10种让学生爱上数学的互动教学方法，通过游戏化和生活实例激发学习兴趣...',
    date: '2023-03-15',
    views: 2341,
    stars: 189,
    avatar: avatars.avatar1,
  },
  {
    title: '传统文化融入语文教学',
    author: '王华 · 教研组长',
    content: '详解如何将传统节日、古代礼仪等文化元素自然融入语文课堂，增强文化认同感...',
    date: '2023-03-12',
    views: 1892,
    stars: 156,
    avatar: avatars.avatar2,
  },
  {
    title: '物理实验创新设计指南',
    author: '张科 · 学科带头人',
    content: '使用简单材料设计有趣的物理实验，让抽象概念变得直观可感，提升教学效果...',
    date: '2023-03-08',
    views: 1654,
    stars: 142,
    avatar: avatars.avatar3,
  },
]);
</script>

<template>
  <div class="resources-section">
    <div class="section-header">
      <h2>推荐资源</h2>
      <el-button text type="primary">更多推荐</el-button>
    </div>

    <div class="resource-cards">
      <el-card class="resource-card" v-for="(resource, index) in resources" :key="index">
        <div class="resource-header">
          <el-avatar :src="resource.avatar"></el-avatar>
          <div class="resource-info">
            <div class="resource-title">{{ resource.title }}</div>
            <div class="resource-author">{{ resource.author }}</div>
          </div>
        </div>
        <div class="resource-content">{{ resource.content }}</div>
        <div class="resource-footer">
          <span class="resource-date">{{ resource.date }}</span>
          <div class="resource-stats">
            <span
              ><el-icon><View /></el-icon> {{ resource.views }}</span
            >
            <span
              ><el-icon><Star /></el-icon> {{ resource.stars }}</span
            >
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<style scoped>
.resources-section {
  margin-bottom: 30px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h2 {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.resource-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.resource-card {
  transition: all 0.3s ease;
}

.resource-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.resource-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  gap: 10px;
}

.resource-info {
  flex: 1;
}

.resource-title {
  font-weight: bold;
  font-size: 16px;
}

.resource-author {
  font-size: 13px;
  color: #666;
}

.resource-content {
  margin-bottom: 15px;
  color: #333;
  height: 80px;
  overflow: hidden;
}

.resource-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #999;
  font-size: 13px;
}

.resource-stats {
  display: flex;
  gap: 15px;
}
</style>
