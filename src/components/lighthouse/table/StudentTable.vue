<script setup lang="ts">
import { ref } from 'vue';
import type { Student } from '@/api';
import SearchBar from './SearchBar.vue';
import { ElCard, ElTable, ElTableColumn, ElAvatar, ElButton, ElProgress, ElPagination } from 'element-plus';
import { Calendar, Plus, Star } from '@element-plus/icons-vue';
import { StudentDetailsDialog, ScoreWorkDialog } from '../index';

defineProps<{
  students: Student[];
  loading: boolean;
  totalCount: number;
}>();

const emit = defineEmits<{
  'update:search': [value: string];
  'update:page': [value: number];
  'view-details': [student: Student];
  'export-data': [];
  'take-attendance': [];
  'add-student': [];
}>();

const searchText = ref('');
const currentPage = ref(1);
const pageSize = ref(10);

const showScoreWorkDialog = ref(false);
const selectedStudent = ref<Student | null>(null);

const handleSearchChange = (value: string) => {
  searchText.value = value;
  currentPage.value = 1; // 搜索时重置页码
  emit('update:search', value);
};

const handlePageChange = (page: number) => {
  currentPage.value = page;
  emit('update:page', page);
};

const getScoreClass = (score: number): string => {
  if (score >= 90) return 'score-excellent';
  if (score >= 80) return 'score-good';
  if (score >= 70) return 'score-average';
  return 'score-poor';
};

const getProgressColor = (value: number): string => {
  if (value >= 90) return '#67C23A';
  if (value >= 80) return '#409EFF';
  if (value >= 70) return '#E6A23C';
  return '#F56C6C';
};

const handleViewDetails = (student: Student) => {
  emit('view-details', student);
};

const handleScoreWork = (student: Student) => {
  selectedStudent.value = student;
  showScoreWorkDialog.value = true;
};

const handleScoreWorkSubmit = (data: any) => {
  console.log('提交成绩和作品数据:', data);
  // 这里可以添加实际的提交逻辑
  showScoreWorkDialog.value = false;
};
</script>

<template>
  <el-card class="student-list-card">
    <template #header>
      <div class="card-header">
        <div class="title-area">
          <div class="title">学生成长追踪</div>
          <div class="header-actions">
            <el-button 
              type="success" 
              @click="emit('add-student')" 
              class="add-student-btn"
              :icon="Plus"
            >
              迎新引航
            </el-button>
            <el-button 
              type="primary" 
              @click="emit('take-attendance')" 
              class="attendance-btn"
              :icon="Calendar"
            >
              考勤点名
            </el-button>
          </div>
        </div>
        <SearchBar
          :value="searchText"
          @update:value="handleSearchChange"
          @export="emit('export-data')"
        />
      </div>
    </template>

    <el-table :data="students" style="width: 100%" v-loading="loading">
      <el-table-column label="学生" min-width="160">
        <template #default="scope">
          <div class="student-info-cell">
            <el-avatar :size="40" :src="scope.row.avatar || '/src/assets/avatar.svg'" />
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
      <el-table-column fixed="right" label="操作" width="220">
        <template #default="{ row }">
          <el-button
            type="primary"
            size="small"
            @click="handleViewDetails(row)"
          >
            查看详情
          </el-button>
          <el-button
            type="warning"
            size="small"
            @click="handleScoreWork(row)"
            class="star-record-btn"
            :icon="Star"
          >
            星光记录
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination-container">
      <el-pagination
        v-model:currentPage="currentPage"
        :page-size="pageSize"
        layout="prev, pager, next, jumper"
        :total="totalCount"
        @current-change="handlePageChange"
      />
    </div>
  </el-card>

  <ScoreWorkDialog
    v-model="showScoreWorkDialog"
    :student="selectedStudent"
    @submit="handleScoreWorkSubmit"
  />
</template>

<style scoped>
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

.title-area {
  display: flex;
  align-items: center;
  gap: 15px;
}

.card-header .title {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.add-student-btn {
  font-size: 14px;
  height: 32px;
  padding: 0 12px;
  background: linear-gradient(135deg, #67C23A 0%, #4CAF50 100%);
  border: none;
  transition: all 0.3s ease;
}

.add-student-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(103, 194, 58, 0.2);
}

.attendance-btn {
  font-size: 14px;
  height: 32px;
  padding: 0 12px;
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

.star-record-btn {
  background: linear-gradient(135deg, #FFA500 0%, #FF8C00 100%);
  border: none;
  color: white;
  transition: all 0.3s ease;
}

.star-record-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 165, 0, 0.3);
}

@media screen and (max-width: 768px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
