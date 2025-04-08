<script setup lang="ts">
defineProps<{
  loading: boolean;
  isEmpty: boolean;
}>();
</script>

<template>
  <div class="content-list" v-loading="loading">
    <slot v-if="!isEmpty"></slot>
    <el-empty v-else description="暂无数据" />
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
