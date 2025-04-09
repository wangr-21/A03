<script setup lang="ts">
import type { StoryItem } from '@/api';

defineProps<{
  story: StoryItem | null;
}>();

const visible = defineModel<boolean>('visible', { required: true });

function formatDate(dateStr: string): string {
  const date = new Date(dateStr);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}
</script>

<template>
  <el-dialog
    v-model="visible"
    :title="story?.title"
    width="60%"
    destroy-on-close
    @update:visible="visible = $event"
  >
    <div v-if="story" class="story-detail">
      <div class="meta-info">
        <el-tag class="meta-tag" size="small" type="success" v-if="story.dynasty">
          朝代: {{ story.dynasty }}
        </el-tag>
        <el-tag class="meta-tag" size="small" v-if="story.period">
          时期: {{ story.period }}
        </el-tag>
        <el-tag class="meta-tag" size="small">主题: {{ story.theme }}</el-tag>
      </div>

      <div class="content-section">
        <h4>故事内容</h4>
        <div class="scrollable-content">
          {{ story.content }}
        </div>
      </div>

      <div v-if="story.moral" class="content-section">
        <h4>寓意</h4>
        <p>{{ story.moral }}</p>
      </div>

      <div v-if="story.reference" class="content-section">
        <h4>参考来源</h4>
        <p>{{ story.reference }}</p>
      </div>

      <div class="footer">
        <span class="created-time">创建于 {{ formatDate(story.created_at) }}</span>
      </div>
    </div>
  </el-dialog>
</template>

<style scoped>
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

    .scrollable-content,
    p {
      background-color: #f8f9fa;
      border: 1px solid #e4e7ed;
      border-radius: 4px;
      padding: 12px;
      line-height: 1.6;
    }

    .scrollable-content {
      max-height: 300px;
      overflow-y: auto;
      padding-right: 12px;

      &::-webkit-scrollbar {
        width: 6px;
      }

      &::-webkit-scrollbar-thumb {
        background-color: #909399;
        border-radius: 3px;
      }

      &::-webkit-scrollbar-track {
        background-color: #f4f4f5;
        border-radius: 3px;
      }
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
