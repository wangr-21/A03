<script setup lang="ts">
import type { RecommendedUser } from '@/api';

defineProps<{
  users: RecommendedUser[];
}>();

const refreshUsers = () => {
  console.log('刷新推荐用户');
  // 实际实现中可以触发父组件刷新推荐用户列表
};
</script>

<template>
  <el-card class="recommend-card">
    <template #header>
      <div class="card-header">
        <h3>推荐合作者</h3>
        <el-button text type="primary" size="small" @click="refreshUsers">换一批</el-button>
      </div>
    </template>
    <div class="recommend-list">
      <div class="recommend-item" v-for="(user, index) in users" :key="index">
        <el-avatar :size="35" :src="user.avatar"></el-avatar>
        <div class="user-info">
          <span class="user-name">{{ user.name }}</span>
          <span class="user-title">{{ user.title }}</span>
        </div>
        <el-button circle icon="Plus" size="small" title="添加关注"></el-button>
      </div>
      <el-empty v-if="!users.length" description="暂无推荐" :image-size="50"></el-empty>
    </div>
  </el-card>
</template>

<style scoped>
.recommend-card {
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
  margin-bottom: 20px;
  border: none;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  font-size: 16px;
  font-weight: bold;
  margin: 0;
  color: #333;
}

.recommend-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.recommend-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.recommend-item:hover {
  background-color: #f5f7fa;
}

.user-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 500;
  font-size: 14px;
  color: #333;
}

.user-title {
  font-size: 12px;
  color: #999;
}
</style>
