<script setup lang="ts">
import { onMounted, reactive, ref, watch } from 'vue';
import { getActivities } from '@/api';
import type { Activity, ActivityFilters } from '@/api';
import ActivityCard from './ActivityCard.vue';
import { ElMessage } from 'element-plus';
import { Refresh } from '@element-plus/icons-vue';

const emit = defineEmits<{
  select: [activity: Activity];
}>();

const isLoading = ref<boolean>(false);
const activities = ref<Activity[]>([]);
const filters = reactive<ActivityFilters>({
  subject: '',
  grade: '',
  activity_type: '',
});

// 活动类型和学科选项
const activityTypes = ['discussion', 'question', 'game'] as const;
const subjects = ['语文', '数学', '英语', '物理', '化学', '生物'] as const;
const grades = ['七年级', '八年级', '九年级'] as const;

const loadActivities = async () => {
  isLoading.value = true;
  try {
    activities.value = await getActivities(filters);
  } catch (error) {
    console.error('Failed to load activities:', error);
    ElMessage.error('加载互动活动数据失败');
  } finally {
    isLoading.value = false;
  }
};

// 获取活动类型显示文本
const getActivityTypeLabel = (type: (typeof activityTypes)[number]): string => {
  const activityTypeMap = {
    discussion: '讨论',
    question: '提问',
    game: '游戏',
  };
  return activityTypeMap[type] || type;
};

// 监听筛选条件变化
watch(filters, () => {
  loadActivities();
});

const handleActivityClick = (activity: Activity) => {
  emit('select', { ...activity });
};

onMounted(() => {
  loadActivities();
});

defineExpose({
  refresh: loadActivities,
});
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
          <el-select v-model="filters.activity_type" placeholder="活动类型" clearable size="small">
            <el-option
              v-for="type in activityTypes"
              :key="type"
              :label="getActivityTypeLabel(type)"
              :value="type"
            />
          </el-select>
          <el-select v-model="filters.subject" placeholder="学科" clearable size="small">
            <el-option
              v-for="subject in subjects"
              :key="subject"
              :label="subject"
              :value="subject"
            />
          </el-select>
          <el-select v-model="filters.grade" placeholder="年级" clearable size="small">
            <el-option v-for="grade in grades" :key="grade" :label="grade" :value="grade" />
          </el-select>
          <el-button type="primary" :icon="Refresh" circle size="small" @click="loadActivities" />
        </div>
      </div>
    </template>

    <div v-loading="isLoading">
      <el-empty v-if="activities.length === 0" description="暂无活动" />
      <div v-else class="activity-list">
        <ActivityCard
          v-for="activity in activities"
          :key="activity.id"
          :activity="activity"
          @click="handleActivityClick(activity)"
        />
      </div>
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
  width: 40%;
}

.activity-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 15px;
  margin-top: 15px;
}
</style>
