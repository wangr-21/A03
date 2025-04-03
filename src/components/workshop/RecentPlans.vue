<script setup lang="ts">
defineProps<{
  recentPlans: Array<{
    title: string;
    subject: string;
    grade: string;
    createdAt: string;
    status: string;
  }>;
}>();
</script>

<template>
  <div class="recent-section">
    <div class="section-header">
      <h2>最近教案</h2>
      <el-button text type="primary">查看全部</el-button>
    </div>

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
          <el-button text type="primary" icon="Edit"></el-button>
          <el-button text type="primary" icon="View"></el-button>
          <el-button text type="danger" icon="Delete"></el-button>
        </template>
      </el-table-column>
    </el-table>
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
</style>
