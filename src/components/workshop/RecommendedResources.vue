<script setup lang="ts">
defineProps<{
  resources: Array<{
    title: string;
    author: string;
    content: string;
    date: string;
    views: number;
    stars: number;
    avatar: string;
  }>;
}>();
</script>

<template>
  <div class="resources-section">
    <div class="section-header">
      <h2>推荐资源</h2>
      <el-button text type="primary">更多推荐</el-button>
    </div>

    <div class="resource-cards">
      <el-card class="resource-card" v-for="(resource, index) in resources" :key="index">
        <div class="resource-header">
          <el-avatar :src="resource.avatar"></el-avatar>
          <div class="resource-info">
            <div class="resource-title">{{ resource.title }}</div>
            <div class="resource-author">{{ resource.author }}</div>
          </div>
        </div>
        <div class="resource-content">{{ resource.content }}</div>
        <div class="resource-footer">
          <span class="resource-date">{{ resource.date }}</span>
          <div class="resource-stats">
            <span
              ><el-icon><View /></el-icon> {{ resource.views }}</span
            >
            <span
              ><el-icon><Star /></el-icon> {{ resource.stars }}</span
            >
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<style scoped>
.resources-section {
  margin-bottom: 30px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h2 {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.resource-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.resource-card {
  transition: all 0.3s ease;
}

.resource-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.resource-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  gap: 10px;
}

.resource-info {
  flex: 1;
}

.resource-title {
  font-weight: bold;
  font-size: 16px;
}

.resource-author {
  font-size: 13px;
  color: #666;
}

.resource-content {
  margin-bottom: 15px;
  color: #333;
  height: 80px;
  overflow: hidden;
}

.resource-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #999;
  font-size: 13px;
}

.resource-stats {
  display: flex;
  gap: 15px;
}
</style>
