<script setup lang="ts">
interface Hotspot {
  title: string;
  content: string;
}

// 热点数据
const hotspot: Hotspot = {
  title: '今日古诗推荐',
  content:
    '《望庐山瀑布》 - 李白\n日照香炉生紫烟，遥看瀑布挂前川。飞流直下三千尺，疑是银河落九天。',
};

const viewHotspotDetail = (): void => {
  console.log('View hotspot detail');
};
</script>

<template>
  <el-card class="hotspot-card">
    <template #header>
      <div class="card-header">
        <h3>
          <el-icon><DataLine /></el-icon> 动态学科热点
        </h3>
      </div>
    </template>
    <div class="hotspot-content">
      <h4>{{ hotspot.title }}</h4>
      <p>{{ hotspot.content }}</p>
      <el-button type="primary" text @click="viewHotspotDetail">查看详情</el-button>
    </div>
  </el-card>
</template>

<style scoped>
.hotspot-card {
  height: 360px;
  display: flex;
  flex-direction: column;
  border-radius: 8px;
  overflow: hidden;
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
  gap: 8px;
}

.card-header h3 .el-icon {
  color: #7353e5;
}

.hotspot-content {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.hotspot-content h4 {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin-bottom: 15px;
}

.hotspot-content p {
  font-size: 16px;
  color: #606266;
  line-height: 1.6;
  white-space: pre-line;
  flex: 1;
}

.hotspot-content .el-button {
  margin-top: 15px;
  align-self: flex-start;
}
</style>
