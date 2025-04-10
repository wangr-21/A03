<script setup lang="ts">
defineProps<{
  loading: boolean;
  isEmpty: boolean;
}>();
</script>

<template>
  <el-empty v-if="isEmpty" description="暂无数据" />
  <div v-else class="content-list" v-loading="loading">
    <slot></slot>
  </div>
</template>

<style scoped>
.content-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-top: 20px;
}
</style>
