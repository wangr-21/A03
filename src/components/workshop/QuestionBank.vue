<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { getQuestions } from '@/api';
import type { Question, QuestionFilters } from '@/api';

interface Difficulty {
  label: string;
  value: string;
}

// --- State for 题海星图 ---
const questionFilters = reactive<QuestionFilters>({
  type: [], // e.g., ['选择题', '填空题']
  difficulty: '', // e.g., 'easy', 'medium', 'hard'
  knowledgePoint: '',
});

const questionTypes = ref<string[]>(['选择题', '填空题', '判断题', '简答题']);
const difficulties = ref<Difficulty[]>([
  { label: '简单', value: 'easy' },
  { label: '中等', value: 'medium' },
  { label: '困难', value: 'hard' },
]);
const knowledgePoints = ref<string[]>(['函数', '几何', '代数', '力学', '光学']); // Placeholder
const questions = ref<Question[]>([]); // Will hold fetched questions
const isQuestionsLoading = ref<boolean>(false);
const questionCurrentPage = ref<number>(1);
const questionPageSize = ref<number>(10);
const totalQuestions = ref<number>(0);

const filterQuestions = async (): Promise<void> => {
  console.log('Filtering questions:', questionFilters);
  isQuestionsLoading.value = true;

  try {
    const response = await getQuestions({
      ...questionFilters,
      page: questionCurrentPage.value,
      pageSize: questionPageSize.value,
    });

    if (response.success) {
      questions.value = response.data.questions;
      totalQuestions.value = response.data.total;
    } else {
      throw new Error('Failed to fetch questions');
    }
  } catch (error) {
    console.error('Error filtering questions:', error);
    ElMessage.error('获取题目失败，请稍后重试');
    questions.value = [];
    totalQuestions.value = 0;
  } finally {
    isQuestionsLoading.value = false;
  }
};

const handleQuestionPageChange = (page: number): void => {
  questionCurrentPage.value = page;
  filterQuestions(); // Refetch questions for the new page
};

// Initial data fetch on mount
onMounted(() => {
  filterQuestions();
});
</script>

<template>
  <el-card class="question-bank-card">
    <template #header>
      <div class="card-header">
        <h3>
          <el-icon><Files /></el-icon> 题海星图 - 智能题库
        </h3>
      </div>
    </template>

    <!-- Filters -->
    <div class="filters">
      <el-form :inline="true" :model="questionFilters">
        <el-form-item label="题型">
          <el-checkbox-group v-model="questionFilters.type">
            <el-checkbox v-for="t in questionTypes" :key="t" :label="t">{{ t }}</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="难度">
          <el-select
            v-model="questionFilters.difficulty"
            placeholder="选择难度"
            clearable
            size="small"
          >
            <el-option
              v-for="d in difficulties"
              :key="d.value"
              :label="d.label"
              :value="d.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="知识点">
          <el-select
            v-model="questionFilters.knowledgePoint"
            placeholder="选择知识点"
            clearable
            filterable
            size="small"
          >
            <el-option v-for="k in knowledgePoints" :key="k" :label="k" :value="k"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="filterQuestions" icon="Search" size="small"
            >筛选题目</el-button
          >
        </el-form-item>
      </el-form>
    </div>

    <!-- Question List Table -->
    <el-table
      :data="questions"
      v-loading="isQuestionsLoading"
      style="width: 100%"
      empty-text="暂无题目，请调整筛选条件"
    >
      <el-table-column prop="type" label="题型" width="100"></el-table-column>
      <el-table-column prop="difficulty" label="难度" width="100">
        <template #default="scope">
          <el-tag
            :type="
              scope.row.difficulty === 'easy'
                ? 'success'
                : scope.row.difficulty === 'medium'
                  ? 'warning'
                  : 'danger'
            "
            size="small"
          >
            {{
              difficulties.find((d) => d.value === scope.row.difficulty)?.label ||
              scope.row.difficulty
            }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="point" label="知识点" width="150"></el-table-column>
      <el-table-column prop="stem" label="题干"></el-table-column>
      <el-table-column label="操作" width="120">
        <template #default>
          <el-button text type="primary" size="small">查看详情</el-button>
          <el-button text type="success" size="small">加入试卷</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- Pagination -->
    <div class="pagination">
      <el-pagination
        background
        layout="prev, pager, next"
        :total="totalQuestions"
        :page-size="questionPageSize"
        v-model:current-page="questionCurrentPage"
        @current-change="handleQuestionPageChange"
      >
      </el-pagination>
    </div>
  </el-card>
</template>

<style scoped>
.question-bank-card {
  margin-bottom: 30px;
}

.filters {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.filters .el-form-item {
  margin-bottom: 10px; /* Adjust spacing for inline form */
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>
