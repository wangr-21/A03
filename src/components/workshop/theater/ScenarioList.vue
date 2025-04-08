<script setup lang="ts">
import type { Scenario } from '@/api/thinking';
import ScenarioCard from './ScenarioCard.vue';

defineProps<{
  scenarios: Scenario[];
}>();

const emit = defineEmits<{
  select: [scenario: Scenario];
}>();

const handleScenarioClick = (scenario: Scenario) => {
  emit('select', scenario);
};
</script>

<template>
  <el-card class="theater-card">
    <template #header>
      <div class="card-header">
        <h3>
          <el-icon><VideoPlay /></el-icon>
          情景模拟沙盘
        </h3>
      </div>
    </template>

    <div class="scenario-list">
      <ScenarioCard
        v-for="scenario in scenarios"
        :key="scenario.id"
        :scenario="scenario"
        @click="handleScenarioClick(scenario)"
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

.scenario-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 15px;
  margin-top: 15px;
}
</style>
