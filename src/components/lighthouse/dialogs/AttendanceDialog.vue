<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import type { Student } from '@/api';
import { ElMessage, ElMessageBox } from 'element-plus';

// Props 定义
const props = defineProps<{
  students: Student[];
  classOptions: { label: string; value: string }[];
}>();

// Model 定义
const visible = defineModel<boolean>('visible', { required: true });

// Emits 定义
const emit = defineEmits<{
  'submit-attendance': [
    data: {
      date: string;
      records: Record<string, string>;
      notes: Record<string, string>;
      class: string;
    },
  ];
}>();

// 状态定义
const selectedDate = ref(new Date().toISOString().split('T')[0]);
const selectedClass = ref('');
const attendanceRecords = ref<Record<string, string>>({});
const attendanceNotes = ref<Record<string, string>>({});
const submitting = ref(false);

// 考勤选项
const attendanceOptions = [
  { label: '出席', value: 'present', type: 'success' },
  { label: '迟到', value: 'late', type: 'warning' },
  { label: '请假', value: 'info', type: 'info' },
  { label: '缺席', value: 'danger', type: 'danger' },
];

// 计算属性
const filteredStudents = computed(() => {
  if (!selectedClass.value) return props.students;
  return props.students.filter((student) => student.class === selectedClass.value);
});

const getPresentCount = computed(() => {
  return filteredStudents.value.filter(
    (student) => attendanceRecords.value[student.id] === 'present',
  ).length;
});

const getAttendanceRate = computed(() => {
  if (filteredStudents.value.length === 0) return 0;
  return Math.round((getPresentCount.value / filteredStudents.value.length) * 100);
});

const getAttendanceRateClass = computed(() => {
  const rate = getAttendanceRate.value;
  if (rate >= 90) return 'excellent';
  if (rate >= 80) return 'good';
  if (rate >= 70) return 'average';
  return 'poor';
});

const canSubmit = computed(() => {
  return filteredStudents.value.every((student) => attendanceRecords.value[student.id]);
});

// 方法
const disableFutureDates = (date: Date) => {
  return date > new Date();
};

const markAllAs = (status: string) => {
  ElMessageBox.confirm(
    `确定将当前显示的所有学生考勤状态标记为"${attendanceOptions.find((opt) => opt.value === status)?.label}"吗？`,
    '批量操作确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    },
  )
    .then(() => {
      filteredStudents.value.forEach((student) => {
        attendanceRecords.value[student.id] = status;
      });
      ElMessage.success('批量标记成功');
    })
    .catch(() => {
      // 用户取消操作
    });
};

const initializeRecords = () => {
  // 初始化所有学生的考勤记录为未选择状态
  props.students.forEach((student) => {
    if (!attendanceRecords.value[student.id]) {
      attendanceRecords.value[student.id] = '';
    }
    if (!attendanceNotes.value[student.id]) {
      attendanceNotes.value[student.id] = '';
    }
  });
};

const handleSubmit = async () => {
  if (!selectedDate.value) {
    ElMessage.warning('请选择考勤日期');
    return;
  }

  if (!canSubmit.value) {
    ElMessage.warning('请确保所有学生都已选择考勤状态');
    return;
  }

  submitting.value = true;
  try {
    await emit('submit-attendance', {
      date: selectedDate.value,
      records: attendanceRecords.value,
      notes: attendanceNotes.value,
      class: selectedClass.value,
    });

    closeDialog();
    ElMessage.success('考勤记录提交成功');
  } catch (error) {
    console.error('提交考勤记录失败:', error);
    ElMessage.error('提交考勤记录失败，请重试');
  } finally {
    submitting.value = false;
  }
};

const closeDialog = () => {
  visible.value = false;
};

// 监听对话框可见性变化
watch(visible, (newVal) => {
  if (newVal) {
    initializeRecords();
    selectedDate.value = new Date().toISOString().split('T')[0];
  }
});
</script>

<template>
  <el-dialog
    title="考勤点名"
    :model-value="visible"
    @update:model-value="visible = $event"
    width="800px"
    class="attendance-dialog"
    :close-on-click-modal="false"
  >
    <div class="attendance-header">
      <div class="filter-group">
        <el-date-picker
          v-model="selectedDate"
          type="date"
          placeholder="选择考勤日期"
          format="YYYY/MM/DD"
          value-format="YYYY-MM-DD"
          :clearable="false"
          :disabled-date="disableFutureDates"
          class="date-picker"
        />
        <el-select v-model="selectedClass" placeholder="选择班级" clearable class="class-select">
          <el-option
            v-for="option in classOptions"
            :key="option.value"
            :label="option.label"
            :value="option.value"
          />
        </el-select>
      </div>

      <div class="quick-actions">
        <span class="action-label">批量操作：</span>
        <div class="action-buttons">
          <el-button
            v-for="option in attendanceOptions"
            :key="option.value"
            :type="option.type"
            size="small"
            @click="markAllAs(option.value)"
          >
            全部标记为{{ option.label }}
          </el-button>
        </div>
      </div>
    </div>

    <el-table :data="filteredStudents" style="width: 100%" :max-height="400" border>
      <el-table-column type="index" label="序号" width="60" align="center" />
      <el-table-column label="学生信息" min-width="200">
        <template #default="{ row }">
          <div class="student-info">
            <el-avatar
              :size="32"
              :src="row.avatar || '/src/assets/avatars/0.svg'"
              class="student-avatar"
            />
            <div class="student-details">
              <div class="student-name">{{ row.name }}</div>
              <div class="student-id">{{ row.id }}</div>
            </div>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="class" label="班级" width="120" align="center" />
      <el-table-column label="考勤状态" width="200" align="center">
        <template #default="{ row }">
          <el-select v-model="attendanceRecords[row.id]" placeholder="请选择" style="width: 120px">
            <el-option
              v-for="option in attendanceOptions"
              :key="option.value"
              :label="option.label"
              :value="option.value"
            >
              <div class="status-option">
                <el-tag :type="option.type" size="small" effect="light">
                  {{ option.label }}
                </el-tag>
              </div>
            </el-option>
          </el-select>
        </template>
      </el-table-column>
      <el-table-column label="备注" min-width="200">
        <template #default="{ row }">
          <el-input
            v-model="attendanceNotes[row.id]"
            placeholder="输入备注信息（选填）"
            size="small"
          />
        </template>
      </el-table-column>
    </el-table>

    <div class="attendance-summary" v-if="filteredStudents.length > 0">
      <div class="summary-item">
        <span class="label">应到人数：</span>
        <span class="value">{{ filteredStudents.length }}</span>
      </div>
      <div class="summary-item">
        <span class="label">实到人数：</span>
        <span class="value">{{ getPresentCount }}</span>
      </div>
      <div class="summary-item">
        <span class="label">出勤率：</span>
        <span class="value" :class="getAttendanceRateClass"> {{ getAttendanceRate }}% </span>
      </div>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="closeDialog">取消</el-button>
        <el-button
          type="primary"
          :loading="submitting"
          :disabled="!canSubmit"
          @click="handleSubmit"
        >
          提交考勤记录
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>
.attendance-dialog {
  --el-dialog-padding-primary: 20px;
}

.attendance-header {
  margin-bottom: 20px;
}

.filter-group {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
}

.date-picker,
.class-select {
  width: 180px;
}

.quick-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.action-label {
  font-weight: 500;
  color: var(--el-text-color-regular);
}

.action-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.student-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.student-avatar {
  flex-shrink: 0;
}

.student-details {
  display: flex;
  flex-direction: column;
}

.student-name {
  font-weight: 500;
  color: var(--el-text-color-primary);
}

.student-id {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.status-option {
  display: flex;
  align-items: center;
}

.attendance-summary {
  margin-top: 20px;
  padding: 15px;
  background-color: var(--el-fill-color-lighter);
  border-radius: 4px;
  display: flex;
  gap: 20px;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.summary-item .label {
  color: var(--el-text-color-regular);
}

.summary-item .value {
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.value.excellent {
  color: var(--el-color-success);
}
.value.good {
  color: var(--el-color-primary);
}
.value.average {
  color: var(--el-color-warning);
}
.value.poor {
  color: var(--el-color-danger);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

@media screen and (max-width: 768px) {
  .filter-group {
    flex-direction: column;
  }

  .date-picker,
  .class-select {
    width: 100%;
  }

  .attendance-summary {
    flex-direction: column;
    gap: 10px;
  }
}
</style>
