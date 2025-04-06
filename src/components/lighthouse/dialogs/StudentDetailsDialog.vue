<script setup lang="ts">
import type { Student } from '@/api';

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
</script>

<template>
  <el-dialog
    v-model="visible"
    @update:model-value="(val: boolean) => visible = val"
    :title="`学生详情 - ${student?.name}`"
    width="500px"
  >
    <div v-if="student" class="student-details">
      <div class="student-avatar">
        <el-avatar :size="80" :src="student.avatar || '/src/assets/avatar.svg'" />
      </div>
      <div class="student-info">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="学号">{{ student.id }}</el-descriptions-item>
          <el-descriptions-item label="姓名">{{ student.name }}</el-descriptions-item>
          <el-descriptions-item label="年级">{{ student.grade }}</el-descriptions-item>
          <el-descriptions-item label="班级">{{ student.class }}</el-descriptions-item>
          <el-descriptions-item label="学业成绩">
            <el-progress :percentage="student.score" :color="getScoreColor(student.score)" />
          </el-descriptions-item>
          <el-descriptions-item label="出勤率">
            <el-progress
              :percentage="student.attendance"
              :color="getAttendanceColor(student.attendance)"
            />
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="closeDialog">关闭</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<style scoped>
.student-details {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.student-avatar {
  margin-bottom: 10px;
}

.student-info {
  width: 100%;
}
</style>
