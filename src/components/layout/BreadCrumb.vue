<script setup lang="ts">
defineProps({
  isMobile: {
    type: Boolean,
    default: false,
  },
});
</script>

<template>
  <div class="breadcrumb" v-if="!isMobile">
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>{{ ($route.meta.title as string) || '当前页面' }}</el-breadcrumb-item>
    </el-breadcrumb>
  </div>
</template>

<style scoped>
.breadcrumb {
  margin-right: auto;
}
</style>
