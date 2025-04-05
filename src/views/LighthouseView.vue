<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { getStudents, getStatistics } from '@/api';
import type { Student, StatItem } from '@/api';

import { PageHeader, StatCards, StudentTable } from '@/components/lighthouse';

// 数据
const stats = ref<StatItem[]>([]);
const students = ref<Student[]>([]);
const loading = ref<boolean>(false);
const searchText = ref<string>('');
const currentPage = ref<number>(1);
const pageSize = ref<number>(10);

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
  ElMessage.info(`查看${student.name}的详细信息`);
};

const evaluateStudent = (student: Student): void => {
  ElMessage.info(`评价${student.name}`);
};

const exportData = (): void => {
  ElMessage.success('正在导出数据...');
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
