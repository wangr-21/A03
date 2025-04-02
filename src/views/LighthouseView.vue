<template>
  <div class="lighthouse-container">
    <div class="page-header">
      <h1 class="page-title">学海灯塔</h1>
      <p class="page-description">智能学生成长追踪与评价系统</p>
    </div>

    <div class="dashboard-content">
      <!-- 统计卡片 -->
      <div class="stats-cards">
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12" :md="6" v-for="(stat, index) in stats" :key="index">
            <el-card class="stat-card" shadow="hover">
              <div class="stat-content">
                <div class="stat-icon" :class="stat.colorClass">
                  <el-icon><component :is="stat.icon" /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stat.value }}</div>
                  <div class="stat-label">{{ stat.label }}</div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 主要内容区域 -->
      <div class="main-content">
        <el-card class="student-list-card">
          <template #header>
            <div class="card-header">
              <div class="title">学生成长追踪</div>
              <div class="controls">
                <el-input
                  v-model="searchText"
                  placeholder="搜索学生"
                  class="search-input"
                  clearable
                >
                  <template #prefix>
                    <el-icon><Search /></el-icon>
                  </template>
                </el-input>
                <el-button type="primary">导出数据</el-button>
              </div>
            </div>
          </template>

          <el-table :data="filteredStudents" style="width: 100%" v-loading="loading">
            <el-table-column label="学生" min-width="160">
              <template #default="scope">
                <div class="student-info-cell">
                  <el-avatar
                    :size="40"
                    :src="scope.row.avatar || '/src/assets/default-avatar.png'"
                  />
                  <div class="student-details">
                    <div class="student-name">{{ scope.row.name }}</div>
                    <div class="student-id">{{ scope.row.id }}</div>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="grade" label="年级" width="100" />
            <el-table-column prop="class" label="班级" width="120" />
            <el-table-column label="平均成绩" width="120">
              <template #default="scope">
                <span :class="getScoreClass(scope.row.score)">{{ scope.row.score }}</span>
              </template>
            </el-table-column>
            <el-table-column label="出勤率" width="180">
              <template #default="scope">
                <el-progress
                  :percentage="scope.row.attendance"
                  :color="getProgressColor(scope.row.attendance)"
                />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180">
              <template #default="scope">
                <el-button size="small" type="primary" @click="viewDetails(scope.row)"
                  >详情</el-button
                >
                <el-button size="small" plain @click="evaluateStudent(scope.row)">评价</el-button>
              </template>
            </el-table-column>
          </el-table>

          <div class="pagination-container">
            <el-pagination
              v-model:currentPage="currentPage"
              :page-size="pageSize"
              layout="prev, pager, next, jumper"
              :total="students.length"
            />
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

// 数据
const stats = ref([
  {
    label: '总学生数',
    value: '256',
    icon: 'User',
    colorClass: 'blue-bg',
  },
  {
    label: '平均成绩',
    value: '86.5',
    icon: 'DataLine',
    colorClass: 'green-bg',
  },
  {
    label: '出勤率',
    value: '97%',
    icon: 'Calendar',
    colorClass: 'orange-bg',
  },
  {
    label: '成长指数',
    value: '+15%',
    icon: 'TrendCharts',
    colorClass: 'purple-bg',
  },
])

const students = ref<
  Array<{
    id: string
    name: string
    avatar?: string
    grade: string
    class: string
    score: number
    attendance: number
  }>
>([])

const loading = ref(true)
const searchText = ref('')
const currentPage = ref(1)
const pageSize = ref(10)

// 计算属性
const filteredStudents = computed(() => {
  if (!searchText.value) {
    return students.value.slice(
      (currentPage.value - 1) * pageSize.value,
      currentPage.value * pageSize.value,
    )
  }

  const filtered = students.value.filter(
    (student) =>
      student.name.toLowerCase().includes(searchText.value.toLowerCase()) ||
      student.id.includes(searchText.value),
  )

  return filtered.slice(
    (currentPage.value - 1) * pageSize.value,
    currentPage.value * pageSize.value,
  )
})

// 方法
const fetchStudents = () => {
  loading.value = true

  // 模拟API请求延迟
  setTimeout(() => {
    students.value = [
      {
        id: '20230001',
        name: '张明',
        grade: '七年级',
        class: '1班',
        score: 92,
        attendance: 98,
        avatar: '/src/assets/avatar1.png',
      },
      {
        id: '20230002',
        name: '李华',
        grade: '七年级',
        class: '1班',
        score: 85,
        attendance: 95,
        avatar: '/src/assets/avatar2.png',
      },
      {
        id: '20230003',
        name: '王芳',
        grade: '七年级',
        class: '2班',
        score: 78,
        attendance: 90,
        avatar: '/src/assets/avatar3.png',
      },
      {
        id: '20230004',
        name: '赵强',
        grade: '七年级',
        class: '2班',
        score: 88,
        attendance: 92,
        avatar: '/src/assets/avatar4.png',
      },
      {
        id: '20230005',
        name: '刘洋',
        grade: '七年级',
        class: '3班',
        score: 76,
        attendance: 85,
        avatar: '/src/assets/avatar5.png',
      },
      {
        id: '20230006',
        name: '陈思',
        grade: '七年级',
        class: '3班',
        score: 95,
        attendance: 99,
        avatar: '/src/assets/avatar6.png',
      },
    ]

    loading.value = false
  }, 1000)
}

const getScoreClass = (score: number): string => {
  if (score >= 90) return 'score-excellent'
  if (score >= 80) return 'score-good'
  if (score >= 70) return 'score-average'
  return 'score-poor'
}

const getProgressColor = (value: number): string => {
  if (value >= 90) return '#67C23A'
  if (value >= 80) return '#409EFF'
  if (value >= 70) return '#E6A23C'
  return '#F56C6C'
}

// 创建一个明确的学生类型接口
interface Student {
  id: string
  name: string
  avatar?: string
  grade: string
  class: string
  score: number
  attendance: number
}

// 使用该接口替换 any 类型
const viewDetails = (student: Student): void => {
  ElMessage.info(`查看${student.name}的详细信息`)
}

const evaluateStudent = (student: Student): void => {
  ElMessage.info(`评价${student.name}`)
}

// 生命周期钩子
onMounted(() => {
  fetchStudents()
})
</script>

<style scoped>
.lighthouse-container {
  padding: 20px;
}

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

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.stats-cards {
  margin-bottom: 10px;
}

.stat-card {
  border-radius: 8px;
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.stat-content {
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
}

.stat-icon .el-icon {
  font-size: 26px;
  color: white;
}

.blue-bg {
  background-color: #409eff;
}

.green-bg {
  background-color: #67c23a;
}

.orange-bg {
  background-color: #e6a23c;
}

.purple-bg {
  background-color: #7353e5;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  line-height: 1.2;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

.main-content {
  margin-top: 10px;
}

.student-list-card {
  border-radius: 8px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 15px;
}

.card-header .title {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}

.card-header .controls {
  display: flex;
  gap: 15px;
  align-items: center;
}

.search-input {
  width: 250px;
}

.student-info-cell {
  display: flex;
  align-items: center;
}

.student-details {
  margin-left: 10px;
}

.student-name {
  font-weight: bold;
  color: #303133;
}

.student-id {
  font-size: 12px;
  color: #909399;
  margin-top: 3px;
}

.score-excellent {
  color: #67c23a;
  font-weight: bold;
}

.score-good {
  color: #409eff;
  font-weight: bold;
}

.score-average {
  color: #e6a23c;
  font-weight: bold;
}

.score-poor {
  color: #f56c6c;
  font-weight: bold;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

@media screen and (max-width: 768px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .card-header .controls {
    width: 100%;
    flex-direction: column;
  }

  .search-input {
    width: 100%;
  }
}
</style>
