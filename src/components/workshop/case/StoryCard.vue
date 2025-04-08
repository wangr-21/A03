<script setup lang="ts">
import type { StoryItem } from '@/api';

defineProps<{
  story: StoryItem;
}>();

const emit = defineEmits<{
  detail: [story: StoryItem];
}>();
</script>

<template>
  <el-card class="story-card" shadow="hover" @click="emit('detail', story)">
    <template #header>
      <div class="card-header">
        <span class="title">{{ story.title }}</span>
        <div class="tags">
          <el-tag size="small" type="success" v-if="story.dynasty">{{ story.dynasty }}</el-tag>
          <el-tag size="small">{{ story.theme }}</el-tag>
        </div>
      </div>
    </template>

    <!-- 卡片简介 -->
    <div class="card-preview">
      <p class="content-preview">
        {{ story.content.substring(0, 80) }}{{ story.content.length > 80 ? '...' : '' }}
      </p>
    </div>
  </el-card>
</template>

<style scoped>
.story-card {
  cursor: pointer;
  transition: transform 0.2s;

  &:hover {
    transform: translateY(-5px);
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;

  .title {
    font-weight: bold;
    font-size: 1.1em;
  }

  .tags {
    display: flex;
    gap: 5px;
  }
}

.card-preview {
  .content-preview {
    color: #666;
    margin: 0;
    display: -webkit-box;
    line-clamp: 3;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}

.story-detail {
  .meta-info {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 20px;
  }

  .content-section {
    margin-bottom: 20px;

    h4 {
      font-size: 1em;
      margin-bottom: 10px;
      color: #303133;
    }

    .scrollable-content {
      max-height: 300px;
      overflow-y: auto;
      padding-right: 10px;
    }
  }

  .footer {
    border-top: 1px solid #ebeef5;
    padding-top: 15px;
    margin-top: 20px;
    color: #909399;
    font-size: 0.9em;
    text-align: right;
  }
}
</style>
