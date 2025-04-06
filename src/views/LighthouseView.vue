<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { getStudents, getStatistics } from '@/api';
import type { Student, StatItem } from '@/api';

import {
  PageHeader,
  StatCards,
  StudentTable,
  StudentDetailsDialog,
  StudentEvaluateDialog,
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
const evaluateDialogVisible = ref<boolean>(false);
const currentStudent = ref<Student | null>(null);
const submittingEvaluation = ref<boolean>(false);

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

const evaluateStudent = (student: Student): void => {
  currentStudent.value = student;
  evaluateDialogVisible.value = true;
};

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const submitEvaluation = async (content: string) => {
  submittingEvaluation.value = true;

  try {
    // 这里应该有一个实际的API调用来提交评价
    // await submitStudentEvaluation(currentStudent.value.id, content);

    // 模拟API调用
    await new Promise((resolve) => setTimeout(resolve, 1000));

    ElMessage.success(`已成功提交对${currentStudent.value?.name}的评价`);
    evaluateDialogVisible.value = false;
  } catch (error) {
    console.error('提交评价失败:', error);
    ElMessage.error('提交评价失败，请稍后重试');
  } finally {
    submittingEvaluation.value = false;
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
        @evaluate-student="evaluateStudent"
        @export-data="exportData"
      />
    </div>

    <!-- 学生详情对话框 -->
    <StudentDetailsDialog v-model:visible="detailsDialogVisible" :student="currentStudent" />

    <!-- 评价对话框 -->
    <StudentEvaluateDialog
      v-model:visible="evaluateDialogVisible"
      :student="currentStudent"
      :submitting="submittingEvaluation"
      @submit="submitEvaluation"
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
