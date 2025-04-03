<script setup lang="ts">
// 统计数据可以从API获取，这里先使用静态数据
const stats = [
  {
    label: '总资源数',
    value: '12,860',
    icon: 'Files',
    colorClass: 'purple-bg',
  },
  {
    label: '本周新增教案',
    value: '+ 152',
    icon: 'DocumentAdd',
    colorClass: 'yellow-bg',
  },
  {
    label: '活跃用户数',
    value: '5,678',
    icon: 'UserFilled',
    colorClass: 'orange-bg',
  },
  {
    label: '党建资源数',
    value: '350',
    icon: 'Flag',
    colorClass: 'red-bg',
  },
];
</script>

<template>
  <div class="stats-cards">
    <el-card class="stats-card" v-for="(stat, index) in stats" :key="index">
      <div class="stats-icon" :class="stat.colorClass">
        <el-icon><component :is="stat.icon" /></el-icon>
      </div>
      <div class="stats-info">
        <div class="stats-number">{{ stat.value }}</div>
        <div class="stats-label">{{ stat.label }}</div>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.stats-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

/* 响应式布局调整 */
@media (max-width: 1399px) {
  .stats-cards {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
  }
}

@media (max-width: 768px) {
  .stats-cards {
    grid-template-columns: 1fr;
    gap: 10px;
  }
}

.stats-card {
  display: flex;
  align-items: center;
  padding: 20px;
  transition:
    transform 0.3s,
    box-shadow 0.3s;
  border-radius: 8px;
  overflow: hidden;
}

.stats-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.stats-icon {
  width: 60px;
  height: 60px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20px;
}

.stats-icon .el-icon {
  font-size: 28px;
  color: white;
}

.purple-bg {
  background-color: #7353e5;
}

.yellow-bg {
  background-color: #ffb64d;
}

.orange-bg {
  background-color: #ff7a5a;
}

.red-bg {
  background-color: #ff5454;
}

.stats-info {
  flex: 1;
}

.stats-number {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.stats-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}
</style>
