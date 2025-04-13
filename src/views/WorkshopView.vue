<script setup lang="ts">
import { ref, onMounted, defineAsyncComponent } from 'vue';

const ToolCards = defineAsyncComponent(() => import('@/components/workshop/ToolCards.vue'));
const LessonPlanGenerator = defineAsyncComponent(
  () => import('@/components/workshop/LessonPlanGenerator.vue'),
);
const ThinkingTheater = defineAsyncComponent(
  () => import('@/components/workshop/ThinkingTheater.vue'),
);
const QuestionBank = defineAsyncComponent(() => import('@/components/workshop/QuestionBank.vue'));
const CaseLibrary = defineAsyncComponent(() => import('@/components/workshop/CaseLibrary.vue'));
const RecentPlans = defineAsyncComponent(() => import('@/components/workshop/RecentPlans.vue'));
const RecommendedResources = defineAsyncComponent(
  () => import('@/components/workshop/RecommendedResources.vue'),
);

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
      // 滚动到思辨剧场互动推荐区域
      document.querySelector('.thinking-theater-card')?.scrollIntoView({ behavior: 'smooth' });
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

const scrollToGenerator = () => {
  // 滚动到灵犀教案生成器区域
  document.querySelector('.generator-card')?.scrollIntoView({ behavior: 'smooth' });
}

// 简化回到顶部逻辑
const showBackToTop = ref(false);

onMounted(() => {
  // 直接显示按钮，不依赖滚动事件
  showBackToTop.value = true;

  // 仍然添加滚动监听，但不影响按钮显示
  window.addEventListener('scroll', () => {
    console.log('Scrolling, position:', window.scrollY);
  });
});

// 修改回到顶部函数，确保能正确滚动
const scrollToTop = () => {
  // 尝试多种滚动方式，确保至少一种能生效

  // 方式1: 使用window.scrollTo
  window.scrollTo({
    top: 0,
    behavior: 'smooth',
  });

  // 方式2: 使用document.documentElement
  document.documentElement.scrollTo({
    top: 0,
    behavior: 'smooth',
  });

  // 方式3: 使用document.body
  document.body.scrollTo({
    top: 0,
    behavior: 'smooth',
  });

  // 方式4: 使用scrollIntoView
  document.querySelector('.page-header')?.scrollIntoView({
    behavior: 'smooth',
    block: 'start',
  });

  console.log('scrollToTop triggered');
};

onMounted(() => {
  showBackToTop.value = true;
});
</script>

<template>
  <div class="workshop-container">
    <div class="page-header">
      <h1 class="page-title">智课工坊</h1>
      <el-button type="primary" icon="Plus" @click="scrollToGenerator">创建新教案</el-button>
    </div>

    <!-- 工具卡片区域 -->
    <ToolCards :tools="tools" @tool-clicked="handleToolClick" />

    <!-- 灵犀教案生成器 -->
    <LessonPlanGenerator />

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

    <!-- 简化自定义回到顶部按钮 -->
    <button v-show="showBackToTop" class="custom-backtop" @click="scrollToTop">
      <el-icon><ArrowUp /></el-icon>
    </button>
  </div>
</template>

<style scoped>
.workshop-container {
  padding: 20px;
  position: relative;
  min-height: 100vh;
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

/* 修改自定义回到顶部按钮样式，确保可见性 */
.custom-backtop {
  position: fixed;
  right: 30px;
  bottom: 30px;
  width: 50px; /* 增大尺寸 */
  height: 50px; /* 增大尺寸 */
  border-radius: 50%;
  background-color: #cacaca; /* 使用更醒目的颜色 */
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3); /* 增强阴影 */
  z-index: 10000; /* 确保最高层级 */
  transition: all 0.3s;
}

.custom-backtop:hover {
  background-color: #ff9980;
  transform: translateY(-5px);
}
</style>
