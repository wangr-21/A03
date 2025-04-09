<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { ArrowLeft, Star, StarFilled, InfoFilled } from '@element-plus/icons-vue';
import type { Question } from '@/api/question';

// 接收题目信息作为props
const props = defineProps<{
  question: Question;
  showHeader?: boolean;
}>();

// 定义事件
const emit = defineEmits([
  'close',
  'add-to-paper',
  'edit',
  'delete',
  'favorite',
  'unfavorite',
  'view-knowledge',
]);

// 判断题目是否已收藏
const isFavorite = ref(false);

// 题目的各种属性
const difficultyClass = computed(() => {
  switch (props.question.difficulty) {
    case '简单':
      return 'success';
    case '中等':
      return 'warning';
    case '困难':
      return 'danger';
    default:
      return 'info';
  }
});

// 选择题选项的映射（A, B, C, D...）
const optionLabels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];

// 添加一个计算属性，用于获取题目解析内容
const explanationContent = computed(() => {
  return props.question.explanation || '暂无解析';
});

// 处理收藏按钮点击
const handleFavoriteClick = () => {
  if (isFavorite.value) {
    emit('unfavorite', props.question.id);
  } else {
    emit('favorite', props.question.id);
  }
  isFavorite.value = !isFavorite.value;
};

// 查看知识点详情
const viewKnowledgePoint = () => {
  emit('view-knowledge', props.question.point);
};

// 添加到试卷
const addToPaper = () => {
  emit('add-to-paper', props.question);
};

// 关闭详情
const close = () => {
  emit('close');
};

// 初始化收藏状态
onMounted(() => {
  // 如果题目本身带有收藏标记，则使用它
  if (props.question.isFavorite !== undefined) {
    isFavorite.value = props.question.isFavorite;
  }
});
</script>

<template>
  <div class="question-detail">
    <!-- 顶部操作栏 -->
    <div v-if="showHeader" class="detail-header">
      <div class="header-left">
        <el-button text @click="close">
          <el-icon><ArrowLeft /></el-icon>
          返回
        </el-button>
      </div>
      <div class="header-right">
        <el-button-group>
          <el-button type="primary" plain @click="addToPaper"> 加入试卷 </el-button>
          <el-button
            :type="isFavorite ? 'warning' : 'default'"
            :icon="isFavorite ? StarFilled : Star"
            plain
            @click="handleFavoriteClick"
          >
            {{ isFavorite ? '已收藏' : '收藏' }}
          </el-button>
          <el-button type="info" plain icon="Share"> 分享 </el-button>
        </el-button-group>
      </div>
    </div>

    <!-- 题目基本信息 -->
    <div class="question-info">
      <div class="info-tags">
        <el-tag size="small">{{ question.type }}</el-tag>
        <el-tag size="small" :type="difficultyClass">{{ question.difficulty }}</el-tag>
        <el-tag size="small" type="info" class="knowledge-tag" @click="viewKnowledgePoint">
          {{ question.point }}
          <el-icon class="info-icon"><InfoFilled /></el-icon>
        </el-tag>
        <el-tag size="small" type="success">{{ question.subject }}</el-tag>
        <el-tag size="small" type="warning">{{ question.grade || '通用' }}</el-tag>
      </div>

      <div class="question-number">题号：{{ question.id }}</div>
    </div>

    <!-- 题目内容区域 -->
    <div class="question-content">
      <!-- 题干 -->
      <div class="question-stem">
        <div class="stem-title">题干：</div>
        <div class="stem-content">{{ question.stem }}</div>
      </div>

      <!-- 选择题选项 -->
      <div v-if="question.type === '选择题'" class="question-options">
        <div class="options-list">
          <div
            v-for="(option, index) in question.options"
            :key="index"
            class="option-item"
            :class="{ 'correct-option': question.answer === optionLabels[index] }"
          >
            <span class="option-label">{{ optionLabels[index] }}.</span>
            <span class="option-content">{{ option }}</span>
          </div>
        </div>
      </div>

      <!-- 题目图片 -->
      <div v-if="question.images && question.images.length > 0" class="question-images">
        <el-image
          v-for="(image, index) in question.images"
          :key="index"
          :src="image"
          :preview-src-list="question.images"
          fit="contain"
          class="question-image"
        />
      </div>

      <!-- 答案和解析 -->
      <div class="question-solution">
        <div class="solution-title">答案：</div>
        <div class="solution-content answer-content">{{ question.answer }}</div>
      </div>

      <div class="question-solution">
        <div class="solution-title">解析：</div>
        <div class="solution-content explanation-content">{{ explanationContent }}</div>
      </div>
    </div>

    <!-- 相关推荐 -->
    <div class="related-section">
      <div class="section-title">相关知识点</div>
      <div class="related-content">
        <el-button type="primary" link @click="viewKnowledgePoint">
          {{ question.point }} 知识点详解
        </el-button>
      </div>
    </div>

    <div class="related-section">
      <div class="section-title">相似题目</div>
      <div class="no-content">
        <el-empty description="暂无相似题目推荐" :image-size="60"></el-empty>
      </div>
    </div>

    <!-- 底部操作区 -->
    <div class="bottom-actions" v-if="!showHeader">
      <el-button type="primary" @click="addToPaper">加入试卷</el-button>
      <el-button :type="isFavorite ? 'warning' : 'default'" @click="handleFavoriteClick">
        {{ isFavorite ? '取消收藏' : '收藏题目' }}
      </el-button>
    </div>
  </div>
</template>

<style scoped>
.question-detail {
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--el-border-color-light);
}

.question-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.info-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.knowledge-tag {
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.knowledge-tag:hover {
  background-color: var(--el-color-info-light-5);
}

.info-icon {
  font-size: 12px;
}

.question-number {
  font-size: 14px;
  color: #888;
}

.question-content {
  margin-bottom: 24px;
}

.question-stem {
  margin-bottom: 20px;
}

.stem-title,
.solution-title {
  font-weight: bold;
  margin-bottom: 8px;
  color: #333;
}

.stem-content {
  line-height: 1.6;
  font-size: 16px;
  white-space: pre-wrap;
}

.question-options {
  margin-top: 16px;
  margin-bottom: 24px;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.option-item {
  display: flex;
  padding: 8px 12px;
  border-radius: 4px;
  background-color: #f9f9f9;
  transition: background-color 0.3s;
}

.correct-option {
  background-color: #f0f9eb;
  border-left: 4px solid var(--el-color-success);
}

.option-label {
  font-weight: bold;
  margin-right: 8px;
  min-width: 24px;
}

.question-images {
  margin: 20px 0;
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.question-image {
  max-width: 250px;
  max-height: 250px;
  border-radius: 4px;
  overflow: hidden;
  border: 1px solid #eee;
}

.question-solution {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px dashed #eee;
}

.answer-content {
  font-weight: bold;
  color: var(--el-color-danger);
  font-size: 16px;
}

.explanation-content {
  line-height: 1.8;
  white-space: pre-wrap;
  color: #666;
}

.related-section {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 16px;
  color: #333;
  display: flex;
  align-items: center;
}

.no-content {
  padding: 20px 0;
  display: flex;
  justify-content: center;
}

.bottom-actions {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: center;
  gap: 16px;
}
</style>
