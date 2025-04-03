<script setup lang="ts">
import { ref } from 'vue';
import ToolCards from '@/components/workshop/ToolCards.vue';
import LessonPlanGenerator from '@/components/workshop/LessonPlanGenerator.vue';
import InteractionRecommender from '@/components/workshop/InteractionRecommender.vue';
import ThinkingTheater from '@/components/workshop/ThinkingTheater.vue';
import QuestionBank from '@/components/workshop/QuestionBank.vue';
import CaseLibrary from '@/components/workshop/CaseLibrary.vue';
import RecentPlans from '@/components/workshop/RecentPlans.vue';
import RecommendedResources from '@/components/workshop/RecommendedResources.vue';

// 组件引用
const thinkingTheaterRef = ref<typeof ThinkingTheater>();

// 工具卡片数据
const tools = ref([
  {
    title: '灵犀教案',
    description: 'AI智能生成完整教案，包含教学目标、重难点和时间轴',
    icon: 'EditPen',
    color: '#6B42E8',
    buttonText: '生成教案',
    buttonType: 'primary' as const,
  },
  {
    title: '思辨剧场',
    description: '智能推荐互动环节与情景模拟，激发学生思考能力',
    icon: 'ChatDotRound',
    color: '#FF7A5A',
    buttonText: '创建剧场',
    buttonType: 'warning' as const,
  },
  {
    title: '题海星图',
    description: '根据知识点智能匹配题目，支持难度和类型筛选',
    icon: 'Document',
    color: '#54D6FF',
    buttonText: '题库探索',
    buttonType: 'info' as const,
  },
  {
    title: '时空走廊',
    description: '传统文化故事库和跨学科案例，拓展教学视野',
    icon: 'Clock',
    color: '#FFB64D',
    buttonText: '浏览案例',
    buttonType: 'success' as const,
  },
]);

// 最近教案数据
const recentPlans = ref([
  {
    title: '《九章算术》与现代数学的联系',
    subject: '数学',
    grade: '初三',
    createdAt: '2023-03-20 14:30',
    status: '已完成',
  },
  {
    title: '春秋战国的历史变革',
    subject: '历史',
    grade: '初二',
    createdAt: '2023-03-18 09:15',
    status: '进行中',
  },
  {
    title: '光的折射与日常生活',
    subject: '物理',
    grade: '初三',
    createdAt: '2023-03-15 16:40',
    status: '已完成',
  },
  {
    title: '诗词中的意象分析',
    subject: '语文',
    grade: '高一',
    createdAt: '2023-03-10 10:20',
    status: '已完成',
  },
]);

// 推荐资源数据
const resources = ref([
  {
    title: '如何让数学课更有趣',
    author: '李明 · 特级教师',
    content: '分享10种让学生爱上数学的互动教学方法，通过游戏化和生活实例激发学习兴趣...',
    date: '2023-03-15',
    views: 2341,
    stars: 189,
    avatar: '/src/assets/avatar1.jpg',
  },
  {
    title: '传统文化融入语文教学',
    author: '王华 · 教研组长',
    content: '详解如何将传统节日、古代礼仪等文化元素自然融入语文课堂，增强文化认同感...',
    date: '2023-03-12',
    views: 1892,
    stars: 156,
    avatar: '/src/assets/avatar2.jpg',
  },
  {
    title: '物理实验创新设计指南',
    author: '张科 · 学科带头人',
    content: '使用简单材料设计有趣的物理实验，让抽象概念变得直观可感，提升教学效果...',
    date: '2023-03-08',
    views: 1654,
    stars: 142,
    avatar: '/src/assets/avatar3.jpg',
  },
]);

// 工具卡片点击处理函数
const handleToolClick = (toolTitle: string) => {
  console.log('Tool clicked:', toolTitle);

  // 根据点击的工具执行不同操作
  switch (toolTitle) {
    case '灵犀教案':
      // 滚动到灵犀教案生成器区域
      document.querySelector('.generator-card')?.scrollIntoView({ behavior: 'smooth' });
      break;
    case '思辨剧场':
      // 打开思辨剧场
      thinkingTheaterRef.value?.openSimulation('classroom');
      break;
    case '题海星图':
      // 滚动到题海星图区域
      document.querySelector('.question-bank-card')?.scrollIntoView({ behavior: 'smooth' });
      break;
    case '时空走廊':
      // 滚动到时空走廊区域
      document.querySelector('.case-library-card')?.scrollIntoView({ behavior: 'smooth' });
      break;
  }
};
</script>

<template>
  <div class="workshop-container">
    <div class="page-header">
      <h1 class="page-title">智课工坊</h1>
      <el-button type="primary" icon="Plus">创建新教案</el-button>
    </div>

    <!-- 工具卡片区域 -->
    <ToolCards :tools="tools" @tool-clicked="handleToolClick" />

    <!-- 灵犀教案生成器 -->
    <LessonPlanGenerator />

    <!-- 思辨剧场 - 互动推荐 -->
    <InteractionRecommender />

    <!-- 思辨剧场组件 -->
    <ThinkingTheater />

    <!-- 题海星图 -->
    <QuestionBank />

    <!-- 时空走廊 -->
    <CaseLibrary />

    <!-- 最近教案 -->
    <RecentPlans :recent-plans="recentPlans" />

    <!-- 推荐资源 -->
    <RecommendedResources :resources="resources" />
  </div>
</template>

<style scoped>
.workshop-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}
</style>
