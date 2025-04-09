<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { ElMessage } from 'element-plus';
import { getStudents, getStatistics } from '@/api';
import type { Student, StatItem } from '@/api';

import {
  PageHeader,
  StatCards,
  StudentTable,
  StudentDetailsDialog,
  AttendanceDialog,
  AddStudentDialog,
} from '@/components/lighthouse';

// 数据
const stats = ref<StatItem[]>([]);
const students = ref<Student[]>([]);
const loading = ref<boolean>(false);
const searchText = ref<string>('');
const currentPage = ref<number>(1);
const pageSize = ref<number>(10);

// 对话框状态变量
const detailsDialogVisible = ref<boolean>(false);
const attendanceDialogVisible = ref<boolean>(false); // 点名对话框状态
const addStudentDialogVisible = ref<boolean>(false); // 添加学生对话框状态
const currentStudent = ref<Student | null>(null);

// 班级选项
const classOptions = computed(() => {
  // 从学生数据中提取唯一的班级选项
  const classSet = new Set<string>();
  students.value.forEach((student) => {
    if (student.class) classSet.add(student.class);
  });

  return Array.from(classSet).map((className) => ({
    label: className,
    value: className,
  }));
});

// 方法
const fetchStudents = async () => {
  loading.value = true;

  try {
    const response = await getStudents({
      search: searchText.value,
      page: currentPage.value,
      pageSize: pageSize.value,
    });

    if (response.success) {
      students.value = response.data.students;
    } else {
      throw new Error('Failed to fetch students');
    }
  } catch (error) {
    console.error('Error fetching students:', error);
    ElMessage.error('获取学生数据失败，请稍后重试');
  } finally {
    loading.value = false;
  }
};

const fetchStatistics = async () => {
  try {
    stats.value = await getStatistics();
  } catch (error) {
    console.error('Error fetching statistics:', error);
    ElMessage.error('获取统计数据失败，请稍后重试');
  }
};

const handleSearchUpdate = (value: string) => {
  searchText.value = value;
  fetchStudents();
};

const handlePageUpdate = (page: number) => {
  currentPage.value = page;
  fetchStudents();
};

const viewDetails = (student: Student): void => {
  currentStudent.value = student;
  detailsDialogVisible.value = true;
};

// 打开点名对话框
const openAttendanceDialog = (): void => {
  attendanceDialogVisible.value = true;
};

// 打开添加学生对话框
const openAddStudentDialog = (): void => {
  addStudentDialogVisible.value = true;
};

// 处理考勤提交
const handleAttendanceSubmit = async (data: {
  date: string;
  records: Record<string, string>;
  class: string;
}) => {
  try {
    // 这里应该有实际的API调用来提交考勤记录
    // await submitAttendanceRecords(data);

    // 模拟API调用延迟
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // 更新出勤率统计（实际项目中应该从API重新获取）
    // 这里只是一个简单示例，实际逻辑可能更复杂
    const presentCount: Record<string, number> = {};
    const totalCount: Record<string, number> = {};

    // 统计出勤人数
    Object.entries(data.records).forEach(([studentId, status]) => {
      const student = students.value.find((s) => s.id === studentId);
      if (student) {
        const studentClass = student.class;
        totalCount[studentClass] = (totalCount[studentClass] || 0) + 1;
        if (status === 'present') {
          presentCount[studentClass] = (presentCount[studentClass] || 0) + 1;
        }
      }
    });

    // 更新学生出勤率（简化示例）
    students.value.forEach((student) => {
      if (data.records[student.id] === 'present') {
        // 假设更新出勤率的逻辑
        const currentAttendance = student.attendance || 0;
        // 这里简化处理，实际应该基于历史记录计算
        student.attendance = Math.min(100, currentAttendance + 1);
      }
    });

    ElMessage.success('考勤记录已成功提交');

    // 刷新统计数据
    fetchStatistics();
  } catch (error) {
    console.error('提交考勤记录失败:', error);
    ElMessage.error('提交考勤记录失败，请稍后重试');
  }
};

// 处理添加学生
const handleAddStudent = async (studentData: Student) => {
  try {
    // 这里应该有实际的API调用来添加学生
    // await addStudent(studentData);

    // 模拟API调用延迟
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // 添加到本地数据（实际应该重新获取数据）
    students.value.unshift({
      ...studentData,
      score: 0,
      attendance: 100,
    });

    // 更新统计数据
    fetchStatistics();

    ElMessage.success('学生添加成功！');
  } catch (error) {
    console.error('添加学生失败:', error);
    ElMessage.error('添加学生失败，请重试');
  }
};

const exportData = (): void => {
  ElMessage.info('正在导出数据...');
  new Promise((resolve) => setTimeout(resolve, 1500)).then(() => {
    ElMessage.success('数据导出成功');
  });
};

// 生命周期钩子
onMounted(() => {
  fetchStudents();
  fetchStatistics();
});
</script>

<template>
  <div class="lighthouse-container">
    <!-- 页面标题组件 -->
    <PageHeader title="学海灯塔" description="智能学生成长追踪与评价系统" />

    <div class="dashboard-content">
      <!-- 统计卡片组件 -->
      <StatCards :stats="stats" />

      <!-- 学生表格组件 -->
      <StudentTable
        :students="students"
        :loading="loading"
        :totalCount="students.length"
        @update:search="handleSearchUpdate"
        @update:page="handlePageUpdate"
        @view-details="viewDetails"
        @export-data="exportData"
        @take-attendance="openAttendanceDialog"
        @add-student="openAddStudentDialog"
      />
    </div>

    <!-- 学生详情对话框 -->
    <StudentDetailsDialog v-model:visible="detailsDialogVisible" :student="currentStudent" />

    <!-- 考勤点名对话框 -->
    <AttendanceDialog
      v-model:visible="attendanceDialogVisible"
      :students="students"
      :classOptions="classOptions"
      @submit-attendance="handleAttendanceSubmit"
    />

    <!-- 添加学生对话框 -->
    <AddStudentDialog
      v-model:visible="addStudentDialogVisible"
      :classOptions="classOptions"
      @submit="handleAddStudent"
    />
  </div>
</template>

<style scoped>
.lighthouse-container {
  padding: 20px;
}

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 25px;
}
</style>
