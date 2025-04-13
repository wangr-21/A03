<script setup lang="ts">
import { useRouter } from 'vue-router';

defineProps<{
  tags: string[];
}>();

const router = useRouter();

// 处理标签点击，跳转到社区页面并带上标签参数
const handleTagClick = (tag: string) => {
  router.push({
    path: '/community',
    query: { tag },
  });
};

const viewAllTags = () => {
  router.push('/community');
};
</script>

<template>
  <div class="hot-topics-container">
    <div class="topics-header">
      <h3>热门话题</h3>
      <el-button text type="primary" size="small" @click="viewAllTags">查看更多</el-button>
    </div>
    <div class="topics-list">
      <el-tag
        v-for="tag in tags"
        :key="tag"
        class="topic-tag"
        effect="plain"
        @click="handleTagClick(tag)"
      >
        # {{ tag }}
      </el-tag>
      <div v-if="!tags.length" class="empty-topics">暂无热门话题</div>
    </div>
  </div>
</template>

<style scoped>
.hot-topics-container {
  background-color: #fff;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  width: 100%;
}

.topics-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.topics-header h3 {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.topics-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.topic-tag {
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 8px 12px;
  margin-bottom: 5px;
}

.topic-tag:hover {
  background-color: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.empty-topics {
  color: #999;
  font-size: 14px;
  padding: 10px 0;
  width: 100%;
  text-align: center;
}

@media (max-width: 768px) {
  .topics-list {
    justify-content: center;
  }
}
</style>
