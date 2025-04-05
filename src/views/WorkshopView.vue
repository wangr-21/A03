<script setup lang="ts">
import { ref } from 'vue';
import {
  ToolCards,
  LessonPlanGenerator,
  InteractionRecommender,
  ThinkingTheater,
  QuestionBank,
  CaseLibrary,
  RecentPlans,
  RecommendedResources,
} from '@/components/workshop';

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
    <RecentPlans />

    <!-- 推荐资源 -->
    <RecommendedResources />
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
