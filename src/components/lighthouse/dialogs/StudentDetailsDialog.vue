<script setup lang="ts">
import { ref } from 'vue';
import type { Student } from '@/api';
import { ElMessageBox } from 'element-plus';
import { avatar0 } from '@/assets/avatars';

defineProps<{
  student: Student | null;
}>();

const visible = defineModel('visible', { required: true });

const closeDialog = () => {
  visible.value = false;
};

// 获取颜色函数
const getScoreColor = (score: number): string => {
  if (score >= 90) return '#67C23A';
  if (score >= 75) return '#409EFF';
  if (score >= 60) return '#E6A23C';
  return '#F56C6C';
};

const getAttendanceColor = (attendance: number): string => {
  if (attendance >= 95) return '#67C23A';
  if (attendance >= 90) return '#409EFF';
  if (attendance >= 80) return '#E6A23C';
  return '#F56C6C';
};

// 模拟历史作品数据
const historyWorks = ref([
  {
    id: 1,
    title: '第一学期期末作品',
    date: '2024-01-15',
    score: 95,
    comment: '作品构思新颖，色彩运用丰富，展现了良好的艺术感染力。',
    files: [
      { name: '水彩画.jpg', url: '/uploads/work1.jpg' },
      { name: '创作说明.pdf', url: '/uploads/desc1.pdf' },
    ],
  },
  {
    id: 2,
    title: '艺术节参赛作品',
    date: '2023-12-10',
    score: 92,
    comment: '主题表达准确，技法运用娴熟，体现了扎实的基本功。',
    files: [{ name: '油画作品.jpg', url: '/uploads/work2.jpg' }],
  },
]);

const activeNames = ref(['1', '2', '3']); // 控制折叠面板的展开状态

const previewWork = (file: { name: string; url: string }) => {
  ElMessageBox.alert(`预览文件: ${file.name}`, '作品预览', {
    confirmButtonText: '关闭',
  });
};
</script>

<template>
  <el-dialog
    v-model="visible"
    @update:model-value="(val: boolean) => (visible = val)"
    :title="`学生详情 - ${student?.name}`"
    width="800px"
    class="student-details-dialog"
  >
    <div v-if="student" class="student-details">
      <el-collapse v-model="activeNames" class="detail-collapse">
        <!-- 基本信息部分 -->
        <el-collapse-item title="基本信息" name="1">
          <div class="basic-info-section">
            <div class="student-avatar">
              <el-avatar :size="100" :src="student.avatar || avatar0" />
            </div>
            <div class="student-info">
              <el-descriptions :column="2" border>
                <el-descriptions-item label="学号">{{ student.id }}</el-descriptions-item>
                <el-descriptions-item label="姓名">{{ student.name }}</el-descriptions-item>
                <el-descriptions-item label="年级">{{ student.grade }}</el-descriptions-item>
                <el-descriptions-item label="班级">{{ student.class }}</el-descriptions-item>
              </el-descriptions>
            </div>
          </div>
        </el-collapse-item>

        <!-- 学习概况部分 -->
        <el-collapse-item title="学习概况" name="2">
          <div class="overview-section">
            <div class="overview-item">
              <h4>学业成绩</h4>
              <el-progress
                :percentage="student.score"
                :color="getScoreColor(student.score)"
                :format="(percentage: number) => `${percentage}分`"
              />
            </div>
            <div class="overview-item">
              <h4>出勤率</h4>
              <el-progress
                :percentage="student.attendance"
                :color="getAttendanceColor(student.attendance)"
                :format="(percentage: number) => `${percentage}%`"
              />
            </div>
            <div class="overview-text">
              <h4>综合评价</h4>
              <p>
                该学生在美术创作方面展现出突出的天赋，善于运用色彩表达情感。课堂参与度高，能够积极配合教学活动。建议在技法的精进上继续努力，相信会有更好的突破。
              </p>
            </div>
          </div>
        </el-collapse-item>

        <!-- 历史作品部分 -->
        <el-collapse-item title="历史作品" name="3">
          <div class="history-works">
            <el-timeline>
              <el-timeline-item
                v-for="work in historyWorks"
                :key="work.id"
                :timestamp="work.date"
                placement="top"
              >
                <el-card class="work-card">
                  <template #header>
                    <div class="work-header">
                      <h3>{{ work.title }}</h3>
                      <el-tag type="success">{{ work.score }}分</el-tag>
                    </div>
                  </template>
                  <div class="work-content">
                    <p class="work-comment">{{ work.comment }}</p>
                    <div class="work-files">
                      <el-button
                        v-for="file in work.files"
                        :key="file.name"
                        type="primary"
                        link
                        @click="previewWork(file)"
                      >
                        {{ file.name }}
                      </el-button>
                    </div>
                  </div>
                </el-card>
              </el-timeline-item>
            </el-timeline>
          </div>
        </el-collapse-item>
      </el-collapse>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="closeDialog">关闭</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<style scoped>
.student-details-dialog :deep(.el-dialog__body) {
  padding: 20px;
}

.student-details {
  max-height: 70vh;
  overflow-y: auto;
}

.detail-collapse {
  border: none;
}

.basic-info-section {
  display: flex;
  gap: 20px;
  align-items: flex-start;
  padding: 10px;
}

.student-info {
  flex: 1;
}

.overview-section {
  padding: 10px;
}

.overview-item {
  margin-bottom: 20px;
}

.overview-item h4 {
  margin: 0 0 10px 0;
  color: #606266;
}

.overview-text {
  margin-top: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.overview-text h4 {
  margin: 0 0 10px 0;
  color: #606266;
}

.overview-text p {
  margin: 0;
  line-height: 1.6;
  color: #606266;
}

.history-works {
  padding: 10px;
}

.work-card {
  margin-bottom: 10px;
}

.work-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.work-header h3 {
  margin: 0;
  font-size: 16px;
  color: #303133;
}

.work-content {
  padding: 10px 0;
}

.work-comment {
  margin: 0 0 15px 0;
  color: #606266;
  line-height: 1.6;
}

.work-files {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

:deep(.el-collapse-item__header) {
  font-size: 16px;
  font-weight: bold;
}

:deep(.el-timeline-item__node) {
  background-color: #409eff;
}

:deep(.el-timeline-item__timestamp) {
  color: #909399;
}
</style>
