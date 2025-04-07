<script setup lang="ts">
import { ref } from 'vue';

const props = defineProps<{
  tags: string[];
  activeTag?: string; // 当前选中的标签
}>();

const emit = defineEmits(['tag-selected']);

// 点击话题标签
const handleTagClick = (tag: string) => {
  emit('tag-selected', tag);
};

const viewAllTags = () => {
  console.log('查看全部话题');
  // 实际实现中可以跳转到话题页面
  emit('tag-selected', ''); // 清除当前选中的标签
};
</script>

<template>
  <el-card class="tags-card">
    <template #header>
      <div class="card-header">
        <h3>热门话题</h3>
        <el-button text type="primary" size="small" @click="viewAllTags">查看更多</el-button>
      </div>
    </template>
    <div class="tag-list">
      <el-tag
        v-for="tag in tags"
        :key="tag"
        class="hot-tag"
        :effect="tag === activeTag ? 'dark' : 'plain'"
        :type="tag === activeTag ? 'primary' : ''"
        @click="handleTagClick(tag)"
        ># {{ tag }}</el-tag
      >
    </div>
    <el-empty v-if="!tags.length" description="暂无热门话题" :image-size="50"></el-empty>
  </el-card>
</template>

<style scoped>
.tags-card {
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
  margin-bottom: 20px;
  border: none;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  width: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 5px;
}

.card-header h3 {
  font-size: 16px;
  font-weight: bold;
  margin: 0;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  padding: 5px;
}

.hot-tag {
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 8px 12px;
  border-radius: 4px;
  margin-bottom: 5px;
}

.hot-tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .tag-list {
    justify-content: center;
  }
}
</style>
