<script setup lang="ts">
import { ref, reactive, onMounted, watch, defineAsyncComponent } from 'vue';
import { ElMessage } from 'element-plus';
import {
  getActivities,
  getScenarios,
  createActivity,
  createScenario,
  type Activity,
  type Scenario,
  type ActivityFilters,
  type CreateActivityRequest,
  type CreateScenarioRequest,
} from '@/api/thinking';

// 异步导入组件
const ActivityList = defineAsyncComponent(() => import('./theater/ActivityList.vue'));
const ActivityDialog = defineAsyncComponent(() => import('./theater/ActivityDialog.vue'));
const ScenarioList = defineAsyncComponent(() => import('./theater/ScenarioList.vue'));
const ScenarioDialog = defineAsyncComponent(() => import('./theater/ScenarioDialog.vue'));
const CreateActivityDialog = defineAsyncComponent(
  () => import('./theater/CreateActivityDialog.vue'),
);
const CreateScenarioDialog = defineAsyncComponent(
  () => import('./theater/CreateScenarioDialog.vue'),
);

// 活动列表
const activities = ref<Activity[]>([]);
const scenarios = ref<Scenario[]>([]);

// 当前选中的活动或场景
const currentActivity = ref<Activity | null>(null);
const currentScenario = ref<Scenario | null>(null);

// 对话框控制
const showActivityDialog = ref(false);
const showScenarioDialog = ref(false);
const showCreateActivityDialog = ref(false);
const showCreateScenarioDialog = ref(false);
const isLoading = ref(false);

// 筛选条件
const activityFilters = reactive<ActivityFilters>({
  subject: '',
  grade: '',
  activity_type: '',
});

// 添加创建状态控制
const isCreatingActivity = ref(false);
const isCreatingScenario = ref(false);

// 加载活动列表
const loadActivities = async () => {
  isLoading.value = true;
  try {
    activities.value = await getActivities(activityFilters);
  } catch (error) {
    console.error('Failed to load activities:', error);
    ElMessage.error('加载互动活动数据失败');
  } finally {
    isLoading.value = false;
  }
};

// 加载场景列表
const loadScenarios = async () => {
  isLoading.value = true;
  try {
    scenarios.value = await getScenarios();
  } catch (error) {
    console.error('Failed to load scenarios:', error);
    ElMessage.error('加载情景模拟数据失败');
  } finally {
    isLoading.value = false;
  }
};

// 监听筛选条件变化
watch(activityFilters, () => {
  loadActivities();
});

// 活动和场景的事件处理
const handleActivitySelect = (activity: Activity) => {
  currentActivity.value = activity;
  showActivityDialog.value = true;
};

const handleScenarioSelect = (scenario: Scenario) => {
  currentScenario.value = scenario;
  showScenarioDialog.value = true;
};

// 创建新活动
const handleCreateActivity = async (data: CreateActivityRequest) => {
  if (isCreatingActivity.value) return;

  isCreatingActivity.value = true;
  try {
    await createActivity(data);
    ElMessage.success('创建成功');
    await loadActivities();
  } catch (error) {
    console.error('创建活动失败:', error);
    ElMessage.error('创建失败，请重试');
  } finally {
    isCreatingActivity.value = false;
  }
};

// 创建新场景
const handleCreateScenario = async (data: CreateScenarioRequest) => {
  if (isCreatingScenario.value) return;

  isCreatingScenario.value = true;
  try {
    await createScenario(data);
    ElMessage.success('创建成功');
    await loadScenarios();
  } catch (error) {
    console.error('创建场景失败:', error);
    ElMessage.error('创建失败，请重试');
  } finally {
    isCreatingScenario.value = false;
  }
};

// 组件挂载时加载数据
onMounted(() => {
  loadActivities();
  loadScenarios();
});
</script>

<template>
  <div class="thinking-theater-card">
    <el-card>
      <template #header>
        <div class="theater-header">
          <h2 class="section-title">思辨剧场</h2>
          <div class="header-actions">
            <el-button
              type="primary"
              @click="showCreateActivityDialog = true"
              :loading="isCreatingActivity"
              :disabled="isCreatingActivity"
              icon="Plus"
            >
              {{ isCreatingActivity ? '创建中...' : '创建互动活动' }}
            </el-button>
            <el-button
              type="warning"
              @click="showCreateScenarioDialog = true"
              :loading="isCreatingScenario"
              :disabled="isCreatingScenario"
              icon="VideoPlay"
            >
              {{ isCreatingScenario ? '创建中...' : '创建情景模拟' }}
            </el-button>
          </div>
        </div>
      </template>

      <!-- 使用活动列表组件 -->
      <ActivityList
        :activities="activities"
        :filters="activityFilters"
        @select="handleActivitySelect"
      />

      <!-- 使用场景列表组件 -->
      <ScenarioList :scenarios="scenarios" @select="handleScenarioSelect" />

      <!-- 使用活动详情对话框组件 -->
      <ActivityDialog v-model:visible="showActivityDialog" :activity="currentActivity" />

      <!-- 使用场景详情对话框组件 -->
      <ScenarioDialog v-model:visible="showScenarioDialog" :scenario="currentScenario" />

      <!-- 添加创建对话框组件 -->
      <CreateActivityDialog
        v-if="showCreateActivityDialog"
        v-model:visible="showCreateActivityDialog"
        @submit="handleCreateActivity"
      />

      <CreateScenarioDialog
        v-if="showCreateScenarioDialog"
        v-model:visible="showCreateScenarioDialog"
        @submit="handleCreateScenario"
      />
    </el-card>
  </div>
</template>

<style scoped>
.thinking-theater-card {
  margin-bottom: 30px;
}

.theater-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  font-size: 22px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 10px;
}
</style>
