<script setup lang="ts">
defineProps<{
  title: string;
  description: string;
}>();
</script>

<template>
  <div class="page-header">
    <h1 class="page-title">{{ title }}</h1>
    <p class="page-description">{{ description }}</p>
  </div>
</template>

<style scoped>
.page-header {
  margin-bottom: 30px;
}

.page-title {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 6px;
}

.page-description {
  font-size: 16px;
  color: #606266;
}
</style>
