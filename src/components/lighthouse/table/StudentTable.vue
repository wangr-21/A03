<script setup lang="ts">
import { ref } from 'vue';
import type { Student } from '@/api';
import SearchBar from './SearchBar.vue';
import { ElCard, ElTable, ElTableColumn, ElAvatar, ElButton, ElProgress, ElPagination } from 'element-plus';
import { Calendar } from '@element-plus/icons-vue';

defineProps<{
  students: Student[];
  loading: boolean;
  totalCount: number;
}>();

const emit = defineEmits<{
  'update:search': [value: string];
  'update:page': [value: number];
  'view-details': [student: Student];
  'evaluate-student': [student: Student];
  'export-data': [];
  'take-attendance': [];
}>();

const searchText = ref('');
const currentPage = ref(1);
const pageSize = ref(10);

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
</script>

<template>
  <el-card class="student-list-card">
    <template #header>
      <div class="card-header">
        <div class="title-area">
        <div class="title">学生成长追踪</div>
          <el-button 
            type="primary" 
            @click="emit('take-attendance')" 
            class="attendance-btn"
            :icon="Calendar"
          >
            考勤点名
          </el-button>
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
      <el-table-column label="操作" width="180">
        <template #default="scope">
          <el-button size="small" type="primary" @click="emit('view-details', scope.row)">
            详情
          </el-button>
          <el-button size="small" plain @click="emit('evaluate-student', scope.row)">
            评价
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

@media screen and (max-width: 768px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
