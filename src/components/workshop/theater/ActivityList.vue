<script setup lang="ts">
import { ref, watch } from 'vue';
import type { Activity, ActivityFilters } from '@/api/thinking';
import ActivityCard from './ActivityCard.vue';

defineProps<{
  activities: Activity[];
}>();

const emit = defineEmits<{
  'select': [activity: Activity];
  'filter': [filters: ActivityFilters];
}>();

// 筛选条件
const filters = ref<ActivityFilters>({
  subject: '',
  grade: '',
  activity_type: '',
});

// 活动类型和学科选项
const activityTypes = ['discussion', 'question', 'game'];
const subjects = ['语文', '数学', '英语', '物理', '化学', '生物'];
const grades = ['七年级', '八年级', '九年级'];

// 获取活动类型显示文本
const getActivityTypeLabel = (type: string): string => {
  const activityTypeMap = {
    discussion: '讨论',
    question: '提问',
    game: '游戏',
  };
  return activityTypeMap[type as keyof typeof activityTypeMap] || type;
};

// 监听筛选条件变化
watch(filters, () => {
  emit('filter', filters.value);
});

const handleActivityClick = (activity: Activity) => {
  emit('select', activity);
};
</script>

<template>
  <el-card class="theater-card">
    <template #header>
      <div class="card-header">
        <h3>
          <el-icon><ChatDotRound /></el-icon>
          互动活动推荐
        </h3>
        <div class="filter-actions">
          <el-select
            v-model="filters.activity_type"
            placeholder="活动类型"
            clearable
            size="small"
          >
            <el-option
              v-for="type in activityTypes"
              :key="type"
              :label="getActivityTypeLabel(type)"
              :value="type"
            />
          </el-select>
          <el-select
            v-model="filters.subject"
            placeholder="学科"
            clearable
            size="small"
          >
            <el-option
              v-for="subject in subjects"
              :key="subject"
              :label="subject"
              :value="subject"
            />
          </el-select>
          <el-select
            v-model="filters.grade"
            placeholder="年级"
            clearable
            size="small"
          >
            <el-option
              v-for="grade in grades"
              :key="grade"
              :label="grade"
              :value="grade"
            />
          </el-select>
        </div>
      </div>
    </template>

    <div class="activity-list">
      <ActivityCard
        v-for="activity in activities"
        :key="activity.id"
        :activity="activity"
        @click="handleActivityClick(activity)"
      />
    </div>
  </el-card>
</template>

<style scoped>
.theater-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 5px;
}

.filter-actions {
  display: flex;
  gap: 10px;
}

.activity-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 15px;
  margin-top: 15px;
}
</style>
