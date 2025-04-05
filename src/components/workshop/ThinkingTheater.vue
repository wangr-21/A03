<script setup lang="ts">
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import { getSimulationScenario } from '@/api';
import type { SimulationScenario } from '@/api';

// --- State for 思辨剧场 - 沙盘 ---
const showSimulationDialog = ref<boolean>(false);
// Holds data for the current simulation
const simulationScenario = ref<SimulationScenario | null>(null);

const openSimulation = async (type: string): Promise<void> => {
  console.log('Opening simulation:', type);

  try {
    const scenario = await getSimulationScenario(type);
    simulationScenario.value = scenario;
    showSimulationDialog.value = true;
  } catch (error) {
    console.error('Error getting simulation scenario:', error);
    ElMessage.error('获取模拟场景失败，请稍后重试');
  }
};

defineExpose({
  // Used in WorkshopView.vue
  openSimulation,
});
</script>

<template>
  <div>
    <!-- 思辨剧场 - 情景模拟沙盘 (Dialog) -->
    <el-dialog
      v-model="showSimulationDialog"
      :title="simulationScenario?.title || '情景模拟'"
      width="60%"
    >
      <div v-if="simulationScenario">
        <p>{{ simulationScenario.description }}</p>
        <!-- TODO: Add interactive elements for the simulation based on scenario data -->
        <el-input
          type="textarea"
          :rows="5"
          placeholder="在此处输入您的模拟操作或回应..."
        ></el-input>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showSimulationDialog = false">关闭</el-button>
          <el-button type="primary" @click="showSimulationDialog = false">提交模拟</el-button>
          <!-- TODO: Add submit logic -->
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
/* 可根据需要添加样式 */
</style>
