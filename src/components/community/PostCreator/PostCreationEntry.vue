<script setup lang="ts">
import { ref } from 'vue';
import { Edit, Picture, Paperclip, QuestionFilled } from '@element-plus/icons-vue';

// const emit = defineEmits(['open-dialog']);
const emit = defineEmits<{
  'open-dialog': [payload: { type?: string; tags?: string[] }];
}>();

// 模拟热门话题数据
const hotTopics = ref(['教学经验分享', '学科融合', '教学案例', '班级管理']);

// 随机占位符文本
const placeholders = [
  '分享您的教学经验、资源或创意...',
  '今天课堂上有什么精彩瞬间？',
  '有什么教学难题需要同行帮助解决？',
  '分享一个教学小技巧吧...',
  '记录您的教学反思与成长...',
];

// 获取随机占位符
const getRandomPlaceholder = () => {
  const index = Math.floor(Math.random() * placeholders.length);
  return placeholders[index];
};

// 打开发帖对话框，可选带上类型
const openPostDialog = (type?: string) => {
  emit('open-dialog', { type });
};

// 带话题打开发帖对话框
const openPostDialogWithTopic = (topic: string) => {
  emit('open-dialog', { tags: [topic] });
};
</script>

<template>
  <el-card class="post-creator-card">
    <div class="creator-main" @click="openPostDialog()">
      <el-avatar class="user-avatar" size="small" src="/src/assets/my_avatar.svg"></el-avatar>
      <div class="input-placeholder">
        <span class="placeholder-text">{{ getRandomPlaceholder() }}</span>
      </div>
    </div>
    <div class="creator-divider"></div>
    <div class="creator-actions">
      <el-button class="action-btn" type="text" @click="openPostDialog('article')">
        <el-icon><Edit /></el-icon>
        <span>发布文章</span>
      </el-button>
      <el-button class="action-btn" type="text" @click="openPostDialog('image')">
        <el-icon><Picture /></el-icon>
        <span>图片分享</span>
      </el-button>
      <el-button class="action-btn" type="text" @click="openPostDialog('resource')">
        <el-icon><Paperclip /></el-icon>
        <span>资源分享</span>
      </el-button>
      <el-button class="action-btn" type="text" @click="openPostDialog('question')">
        <el-icon><QuestionFilled /></el-icon>
        <span>提问求助</span>
      </el-button>
    </div>
    <div class="hot-topics" v-if="hotTopics.length > 0">
      <div class="topics-title">热门话题:</div>
      <div class="topics-list">
        <el-tag
          v-for="topic in hotTopics"
          :key="topic"
          size="small"
          effect="plain"
          class="topic-tag"
          @click="openPostDialogWithTopic(topic)"
        >
          # {{ topic }}
        </el-tag>
      </div>
    </div>
  </el-card>
</template>

<style scoped>
.post-creator-card {
  background: var(--el-bg-color);
  border-radius: 8px;
  margin-bottom: 16px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  transition: box-shadow 0.3s;
}

.post-creator-card:hover {
  box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.1);
}

.creator-main {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  cursor: pointer;
}

.user-avatar {
  flex-shrink: 0;
  border: 2px solid var(--el-color-primary-light-8);
}

.input-placeholder {
  flex-grow: 1;
  background: var(--el-fill-color-lighter);
  border-radius: 18px;
  padding: 10px 16px;
  transition: all 0.3s ease;
}

.placeholder-text {
  color: var(--el-text-color-secondary);
  font-size: 14px;
}

.input-placeholder:hover {
  background: var(--el-fill-color-dark);
  transform: translateY(-2px);
}

.creator-divider {
  height: 1px;
  background: var(--el-border-color-lighter);
  margin: 0 16px;
}

.creator-actions {
  display: flex;
  padding: 12px 8px;
  gap: 8px;
  justify-content: space-around;
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  height: 36px;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: var(--el-fill-color-light);
  color: var(--el-color-primary);
}

.action-btn .el-icon {
  font-size: 16px;
}

.action-btn span {
  font-size: 14px;
  color: var(--el-text-color-regular);
}

.hot-topics {
  padding: 0 16px 16px;
  margin-top: 4px;
}

.topics-title {
  font-size: 13px;
  color: var(--el-text-color-secondary);
  margin-bottom: 8px;
}

.topics-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.topic-tag {
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
}

.topic-tag:hover {
  background-color: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
  transform: scale(1.05);
}
</style>
