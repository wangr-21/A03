<script setup lang="ts">
import type { Scenario } from '@/api/thinking';

// 场景类型映射
const scenarioTypeMap = {
  historical: { label: '历史情境', tag: 'warning' },
  literary: { label: '文学情境', tag: 'success' },
  scientific: { label: '科学情境', tag: 'info' },
} as const;

const getScenarioTypeLabel = (type: string): string => {
  return scenarioTypeMap[type as keyof typeof scenarioTypeMap]?.label || type;
};

const getScenarioTypeTag = (type: string): string => {
  return scenarioTypeMap[type as keyof typeof scenarioTypeMap]?.tag || 'info';
};

defineProps<{
  scenario: Scenario;
}>();
</script>

<template>
  <el-card class="scenario-item" shadow="hover">
    <div class="scenario-item-header">
      <h4>{{ scenario.title }}</h4>
      <el-tag :type="getScenarioTypeTag(scenario.scenario_type)">
        {{ getScenarioTypeLabel(scenario.scenario_type) }}
      </el-tag>
    </div>
    <p class="scenario-description">{{ scenario.background }}</p>
    <div class="scenario-meta">
      <el-tag size="small" effect="plain">{{ scenario.subject }}</el-tag>
      <el-tag size="small" effect="plain">{{ scenario.grade }}</el-tag>
    </div>
  </el-card>
</template>

<style scoped>
.scenario-item {
  cursor: pointer;
  transition: all 0.3s ease;
}

.scenario-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.scenario-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.scenario-item-header h4 {
  margin: 0;
  font-size: 16px;
  font-weight: bold;
}

.scenario-description {
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

.scenario-meta {
  display: flex;
  gap: 8px;
  margin-top: 10px;
}
</style>
