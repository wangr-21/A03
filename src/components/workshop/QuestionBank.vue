<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { Files, Document, Timer, Edit, View, Delete } from '@element-plus/icons-vue';
import { getQuestions } from '@/api';
import type { Question, QuestionFilters } from '@/api';
import PaperPreview from './PaperPreview.vue';
import PaperHistory from './PaperHistory.vue';

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

const paperPreviewRef = ref<InstanceType<typeof PaperPreview>>();
const paperPreviewVisible = ref<boolean>(false);
const paperHistoryVisible = ref<boolean>(false);

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

const addToPaper = (question: Question) => {
  if (paperPreviewRef.value) {
    const existingQuestions = paperPreviewRef.value.selectedQuestions;
    if (existingQuestions.some(q => q.id === question.id)) {
      ElMessage.warning('该题目已在试卷中');
      return;
    }
    existingQuestions.push(question);
    ElMessage.success('已添加到试卷');
  }
};

const showPaperPreview = () => {
  paperPreviewVisible.value = true;
};

const handlePreviewClose = () => {
  paperPreviewVisible.value = false;
};

const showPaperHistory = () => {
  paperHistoryVisible.value = true;
};

const handleHistoryClose = () => {
  paperHistoryVisible.value = false;
};

// Initial data fetch on mount
onMounted(() => {
  filterQuestions();
});
</script>

<template>
  <div class="workshop-container">
    <el-card class="question-bank-card">
      <template #header>
        <div class="card-header">
          <div class="header-content">
            <h3 class="header-title">
              <el-icon><Files /></el-icon> 题海星图 - 智能题库
            </h3>
            <div class="header-actions">
              <el-button type="primary" @click="showPaperPreview" class="action-button">
                <el-icon class="button-icon"><Document /></el-icon>
                试卷预览
                <template #suffix>
                  <el-badge
                    v-if="paperPreviewRef?.selectedQuestions?.length"
                    :value="paperPreviewRef.selectedQuestions.length"
                    class="preview-badge"
                  />
                </template>
              </el-button>
              <el-button type="info" plain @click="showPaperHistory" class="action-button">
                <el-icon class="button-icon"><Timer /></el-icon>
                历史试卷
              </el-button>
            </div>
          </div>
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
              style="width: 120px"
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
              style="width: 160px"
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
      <div class="table-container">
        <el-table
          :data="questions"
          v-loading="isQuestionsLoading"
          style="width: 100%"
          empty-text="暂无题目，请调整筛选条件"
        >
          <el-table-column type="index" width="50" label="序号"></el-table-column>
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
          <el-table-column label="操作" width="180" fixed="right">
            <template #default="scope">
              <div class="operation-buttons">
                <el-button text type="primary" size="small">查看详情</el-button>
                <el-button text type="success" size="small" @click="addToPaper(scope.row)">加入试卷</el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- Pagination -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="questionCurrentPage"
          v-model:page-size="questionPageSize"
          :page-sizes="[10, 20, 30, 50]"
          :total="totalQuestions"
          layout="total, sizes, prev, pager, next"
          @size-change="handleQuestionPageChange"
          @current-change="handleQuestionPageChange"
        />
      </div>
    </el-card>

    <!-- 试卷预览弹窗 -->
    <el-dialog
      v-model="paperPreviewVisible"
      title="试卷预览"
      width="65%"
      :destroy-on-close="false"
      @close="handlePreviewClose"
    >
      <PaperPreview ref="paperPreviewRef" />
    </el-dialog>

    <!-- 试卷历史弹窗 -->
    <el-dialog
      v-model="paperHistoryVisible"
      title="试卷历史"
      width="65%"
      :destroy-on-close="false"
      @close="handleHistoryClose"
    >
      <PaperHistory />
    </el-dialog>
  </div>
</template>

<style scoped>
.workshop-container {
  padding: 0;
  margin-bottom: 16px;
}

.question-bank-card {
  margin: 0;
  border-radius: 8px;
  box-shadow: var(--el-box-shadow-lighter);
  background-color: var(--el-bg-color);
}

.question-bank-card :deep(.el-card__header) {
  padding: 0;
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.card-header {
  padding: 16px 24px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-height: 32px;
}

.header-title {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
  color: var(--el-text-color-primary);
  display: flex;
  align-items: center;
  gap: 8px;
  line-height: 1.5;
}

.header-title .el-icon {
  font-size: 18px;
  margin-right: 4px;
}

.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.action-button {
  display: inline-flex;
  align-items: center;
  height: 32px;
  padding: 0 16px;
  font-size: 14px;
}

.button-icon {
  margin-right: 4px;
  font-size: 16px;
}

.preview-badge {
  margin-left: 8px;
}

.question-bank-card :deep(.el-card__body) {
  padding: 24px;
}

.filters {
  margin: 0 0 24px;
  padding: 0;
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.filters :deep(.el-form) {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  padding-bottom: 24px;
}

.filters :deep(.el-form-item) {
  margin: 0;
}

.filters :deep(.el-form-item__label) {
  font-size: 14px;
  color: var(--el-text-color-regular);
}

.table-container {
  margin: 0;
  min-height: 300px;
}

:deep(.el-table) {
  --el-table-border-color: var(--el-border-color-lighter);
  --el-table-header-bg-color: var(--el-fill-color-light);
}

:deep(.el-table th) {
  font-weight: 500;
  background-color: var(--el-fill-color-light);
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.operation-buttons {
  display: flex;
  gap: 12px;
  align-items: center;
}

.operation-buttons :deep(.el-button) {
  padding: 4px 12px;
  min-width: 68px;
  justify-content: center;
}

.pagination {
  margin-top: 24px;
  padding-top: 16px;
  text-align: center;
  border-top: 1px solid var(--el-border-color-lighter);
}

:deep(.el-pagination) {
  justify-content: center;
  padding: 0;
}

:deep(.el-dialog) {
  --el-dialog-padding-primary: 0;
  border-radius: 8px;
  overflow: hidden;
}

:deep(.el-dialog__header) {
  margin: 0;
  padding: 16px 24px;
  border-bottom: 1px solid var(--el-border-color-lighter);
}

:deep(.el-dialog__body) {
  padding: 24px;
}
</style>