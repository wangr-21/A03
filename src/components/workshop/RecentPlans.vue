<script setup lang="ts">
import { ref } from 'vue';

interface RecentPlan {
  title: string;
  subject: string;
  grade: string;
  createdAt: string;
  status: string;
}

// 最近教案数据
const recentPlans = ref<RecentPlan[]>([
  {
    title: '《九章算术》与现代数学的联系',
    subject: '数学',
    grade: '初三',
    createdAt: '2023-03-20 14:30',
    status: '已完成',
  },
  {
    title: '春秋战国的历史变革',
    subject: '历史',
    grade: '初二',
    createdAt: '2023-03-18 09:15',
    status: '进行中',
  },
  {
    title: '光的折射与日常生活',
    subject: '物理',
    grade: '初三',
    createdAt: '2023-03-15 16:40',
    status: '已完成',
  },
  {
    title: '诗词中的意象分析',
    subject: '语文',
    grade: '高一',
    createdAt: '2023-03-10 10:20',
    status: '已完成',
  },
]);
</script>

<template>
  <div class="recent-section">
    <el-card>
      <template #header>
        <div class="section-header">
          <h2>最近教案</h2>
          <el-button text type="primary">查看全部</el-button>
        </div>
      </template>

      <el-table :data="recentPlans" style="width: 100%">
        <el-table-column prop="title" label="教案名称" min-width="200">
          <template #default="scope">
            <div class="plan-title-cell">
              <el-icon>
                <Document />
              </el-icon>
              <span>{{ scope.row.title }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="subject" label="学科" width="120"></el-table-column>
        <el-table-column prop="grade" label="年级" width="120"></el-table-column>
        <el-table-column prop="createdAt" label="创建时间" width="180"></el-table-column>
        <el-table-column prop="status" label="状态" width="120">
          <template #default="scope">
            <el-tag :type="scope.row.status === '已完成' ? 'success' : 'warning'">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default>
            <div class="operation-buttons">
              <el-button text type="primary" icon="Edit" size="small"></el-button>
              <el-button text type="primary" icon="View" size="small"></el-button>
              <el-button text type="danger" icon="Delete" size="small"></el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<style scoped>
.recent-section {
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

.plan-title-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.operation-buttons {
  display: flex;
  align-items: center;
  gap: 8px;
}

.operation-buttons :deep(.el-button) {
  padding: 6px;
  min-width: 32px;
  height: 32px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.operation-buttons :deep(.el-icon) {
  font-size: 16px;
}
</style>
