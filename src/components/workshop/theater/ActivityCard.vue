<script setup lang="ts">
import type { Activity } from '@/api/thinking';

// 活动类型标签和文本映射
const activityTypeMap = {
  discussion: { label: '讨论', tag: 'success' },
  question: { label: '提问', tag: 'primary' },
  game: { label: '游戏', tag: 'warning' },
} as const;

const getActivityTypeLabel = (type: string): string => {
  return activityTypeMap[type as keyof typeof activityTypeMap]?.label || type;
};

const getActivityTypeTag = (type: string): string => {
  return activityTypeMap[type as keyof typeof activityTypeMap]?.tag || 'info';
};

defineProps<{
  activity: Activity;
}>();
</script>

<template>
  <el-card class="activity-item" shadow="hover">
    <div class="activity-item-header">
      <el-tag :type="getActivityTypeTag(activity.activity_type)">
        {{ getActivityTypeLabel(activity.activity_type) }}
      </el-tag>
      <h4>{{ activity.title }}</h4>
    </div>
    <p class="activity-preview">{{ activity.description }}</p>
    <div class="activity-meta">
      <el-tag size="small" effect="plain">{{ activity.subject }}</el-tag>
      <el-tag size="small" effect="plain">{{ activity.grade }}</el-tag>
      <el-tag size="small" effect="plain">{{ activity.duration }}分钟</el-tag>
    </div>
  </el-card>
</template>

<style scoped>
.activity-item {
  cursor: pointer;
  transition: all 0.3s ease;
}

.activity-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.activity-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.activity-item-header h4 {
  margin: 0;
  font-size: 16px;
  font-weight: bold;
}

.activity-preview {
  color: #666;
  margin-bottom: 10px;
  height: 40px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
}

.activity-meta {
  display: flex;
  gap: 8px;
  margin-top: 10px;
}
</style>
