<script setup lang="ts">
import { ref, watch } from 'vue';

const props = defineProps<{
  value: string;
}>();

const emit = defineEmits<{
  'update:value': [value: string];
  'export': [];
}>();

const localValue = ref(props.value);

watch(() => props.value, (newVal) => {
  localValue.value = newVal;
});

watch(localValue, (newVal) => {
  emit('update:value', newVal);
});

const exportData = () => {
  emit('export');
};
</script>

<template>
  <div class="controls">
    <el-input
      v-model="localValue"
      placeholder="搜索学生"
      class="search-input"
      clearable
    >
      <template #prefix>
        <el-icon><Search /></el-icon>
      </template>
    </el-input>
    <el-button type="primary" @click="exportData">导出数据</el-button>
  </div>
</template>

<style scoped>
.controls {
  display: flex;
  gap: 15px;
  align-items: center;
}

.search-input {
  width: 250px;
}

@media screen and (max-width: 768px) {
  .controls {
    width: 100%;
    flex-direction: column;
  }

  .search-input {
    width: 100%;
  }
}
</style>
