<script setup lang="ts">
import { getScenarios, type Scenario } from '@/api';
import ScenarioCard from './ScenarioCard.vue';
import { onMounted, ref } from 'vue';
import { ElMessage } from 'element-plus';
import { Refresh } from '@element-plus/icons-vue';

const isLoading = ref<boolean>(false);
const scenarios = ref<Scenario[]>([]);

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

const emit = defineEmits<{
  select: [scenario: Scenario];
}>();

const handleScenarioClick = (scenario: Scenario) => {
  emit('select', { ...scenario });
};

onMounted(() => {
  loadScenarios();
});

defineExpose({
  refresh: loadScenarios,
});
</script>

<template>
  <el-card class="theater-card">
    <template #header>
      <div class="card-header">
        <h3>
          <el-icon><VideoPlay /></el-icon>
          情景模拟沙盘
        </h3>
        <el-button type="primary" :icon="Refresh" circle size="small" @click="loadScenarios" />
      </div>
    </template>

    <div v-loading="isLoading">
      <el-empty v-if="scenarios.length === 0" description="暂无情景" />
      <div v-else class="scenario-list">
        <ScenarioCard
          v-for="scenario in scenarios"
          :key="scenario.id"
          :scenario="scenario"
          @click="handleScenarioClick(scenario)"
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

.scenario-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 15px;
  margin-top: 15px;
}
</style>
