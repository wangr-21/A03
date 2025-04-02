<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import {
  ElDialog,
  ElButton,
  ElInput,
  ElSelect,
  ElOption,
  ElTable,
  ElTableColumn,
  ElPagination,
  ElTag,
  ElCheckboxGroup,
  ElCheckbox,
} from 'element-plus';
import {
  generateLessonPlan,
  getRecommendedInteractions,
  getQuestions,
  getCases,
  getSimulationScenario,
} from '@/api';
import type {
  PlanForm,
  InteractionItem,
  Question,
  QuestionFilters,
  CaseItem,
  CaseFilters,
  SimulationScenario,
} from '@/api';

interface TeachingStyle {
  value: string;
  label: string;
}

interface Difficulty {
  label: string;
  value: string;
}

// Reactive form data for lesson plan generation
const planForm = reactive<PlanForm>({
  subject: '',
  grade: '',
  topic: '',
  duration: 60, // Default duration in minutes
  objectives: '', // Learning objectives
  keyPoints: '', // Key and difficult points
  teachingStyle: 'interactive', // e.g., lecture, interactive, project-based
  outputFormat: 'full', // full or concise
});

// Ref for the generated lesson plan content
const generatedPlan = ref<string | null>(null);
const isGenerating = ref<boolean>(false);

// Placeholder subjects and grades (replace with actual data source if needed)
const subjects = ref<string[]>([
  '语文',
  '数学',
  '英语',
  '物理',
  '化学',
  '历史',
  '地理',
  '生物',
  '政治',
]);
const grades = ref<string[]>([
  '一年级',
  '二年级',
  '三年级',
  '四年级',
  '五年级',
  '六年级',
  '初一',
  '初二',
  '初三',
  '高一',
  '高二',
  '高三',
]);
const teachingStyles = ref<TeachingStyle[]>([
  { value: 'interactive', label: '互动探究式' },
  { value: 'lecture', label: '讲授式' },
  { value: 'project', label: '项目式' },
  { value: 'inquiry', label: '问题驱动式' },
]);

// Ref for recommended interactions
const recommendedInteractions = ref<InteractionItem[]>([]);
const isLoadingInteractions = ref<boolean>(false);

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

// --- State for 时空走廊 ---
const caseFilters = reactive<CaseFilters>({
  category: '', // e.g., '传统故事', '跨学科案例'
  era: '', // e.g., '唐代', '宋代'
  theme: '',
});
const caseCategories = ref<string[]>(['传统故事', '跨学科案例']);
const eras = ref<string[]>(['先秦', '秦汉', '魏晋', '隋唐', '宋元', '明清']); // Placeholder
const themes = ref<string[]>(['爱国主义', '科学探索', '文化艺术', '哲学思辨']); // Placeholder
const cases = ref<CaseItem[]>([]); // Will hold fetched cases
const isCasesLoading = ref<boolean>(false);

// --- State for 思辨剧场 - 沙盘 ---
const showSimulationDialog = ref<boolean>(false);
const simulationScenario = ref<SimulationScenario | null>(null); // Holds data for the current simulation

// Function to handle lesson plan generation
const onGenerateLessonPlan = async (): Promise<void> => {
  if (!planForm.subject || !planForm.grade || !planForm.topic) {
    ElMessage.warning('请至少填写学科、年级和课题！');
    return;
  }

  isGenerating.value = true;
  generatedPlan.value = null; // Clear previous result
  console.log('Generating lesson plan with data:', planForm);

  try {
    const response = await generateLessonPlan(planForm);

    if (response.success) {
      // Format the content slightly for display (e.g., handling newlines)
      generatedPlan.value = response.data.content.replace(/\n/g, '<br/>');
      ElMessage.success('教案生成成功！');
    } else {
      throw new Error('AI generation failed');
    }
  } catch (error) {
    console.error('Error generating lesson plan:', error);
    ElMessage.error('教案生成失败，请稍后重试。');
  } finally {
    isGenerating.value = false;
  }
};

// Function to fetch recommended interactions
const fetchRecommendedInteractions = async (): Promise<void> => {
  if (!generatedPlan.value) return; // Ensure plan exists

  isLoadingInteractions.value = true;
  recommendedInteractions.value = []; // Clear previous recommendations
  console.log('Fetching recommended interactions based on:', planForm.topic);

  try {
    const response = await getRecommendedInteractions(planForm.topic);

    if (response.success) {
      recommendedInteractions.value = response.data;
      ElMessage.success('互动推荐获取成功！');
    } else {
      throw new Error('Interaction recommendation failed');
    }
  } catch (error) {
    console.error('Error fetching interactions:', error);
    ElMessage.error('获取互动推荐失败，请稍后重试。');
  } finally {
    isLoadingInteractions.value = false;
  }
};

// --- Placeholder Functions ---
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

const filterCases = async (): Promise<void> => {
  console.log('Filtering cases:', caseFilters);
  isCasesLoading.value = true;

  try {
    const response = await getCases(caseFilters);

    if (response.success) {
      cases.value = response.data.cases;
    } else {
      throw new Error('Failed to fetch cases');
    }
  } catch (error) {
    console.error('Error filtering cases:', error);
    ElMessage.error('获取案例失败，请稍后重试');
    cases.value = [];
  } finally {
    isCasesLoading.value = false;
  }
};

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const openSimulation = async (type: string): Promise<void> => {
  console.log('Opening simulation:', type);

  try {
    const scenario = await getSimulationScenario(type);
    simulationScenario.value = scenario;
    showSimulationDialog.value = true;
  } catch (error) {
    console.error('Error getting simulation scenario:', error);
    ElMessage.error('获取模拟场景失败，请稍后重试');
  }
};

const viewCaseDetails = (caseId: number): void => {
  console.log('Viewing case details:', caseId);
  // TODO: Navigate to case detail page or open modal
};

// Initial data fetch on mount (optional)
onMounted(() => {
  filterQuestions();
  filterCases();
});
</script>

<template>
  <div class="workshop-container">
    <div class="page-header">
      <h1 class="page-title">智课工坊</h1>
      <el-button type="primary" icon="Plus">创建新教案</el-button>
    </div>

    <!-- 工具卡片区域 -->
    <div class="tool-cards">
      <el-card class="tool-card" v-for="(tool, index) in tools" :key="index">
        <div class="tool-icon">
          <el-icon :size="40" :color="tool.color"><component :is="tool.icon" /></el-icon>
        </div>
        <h3 class="tool-title">{{ tool.title }}</h3>
        <p class="tool-desc">{{ tool.description }}</p>
        <el-button class="tool-btn" :type="tool.buttonType">{{ tool.buttonText }}</el-button>
      </el-card>
    </div>

    <!-- 灵犀教案 - 生成区域 -->
    <el-card class="generator-card">
      <template #header>
        <div class="card-header">
          <h3>
            <el-icon><EditPen /></el-icon> 灵犀教案生成器
          </h3>
        </div>
      </template>
      <el-form :model="planForm" label-width="100px" class="generator-form">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="学科" required>
              <el-select v-model="planForm.subject" placeholder="请选择学科">
                <el-option
                  v-for="item in subjects"
                  :key="item"
                  :label="item"
                  :value="item"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="年级" required>
              <el-select v-model="planForm.grade" placeholder="请选择年级">
                <el-option
                  v-for="item in grades"
                  :key="item"
                  :label="item"
                  :value="item"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="课题/单元" required>
          <el-input v-model="planForm.topic" placeholder="请输入教学课题或单元名称"></el-input>
        </el-form-item>
        <el-form-item label="教学目标">
          <el-input
            type="textarea"
            :rows="2"
            v-model="planForm.objectives"
            placeholder="简述主要教学目标（可选）"
          ></el-input>
        </el-form-item>
        <el-form-item label="重难点">
          <el-input
            type="textarea"
            :rows="2"
            v-model="planForm.keyPoints"
            placeholder="简述教学重难点（可选）"
          ></el-input>
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="课时(分钟)">
              <el-input-number v-model="planForm.duration" :min="15" :max="120" :step="5" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="教学风格">
              <el-select v-model="planForm.teachingStyle">
                <el-option
                  v-for="style in teachingStyles"
                  :key="style.value"
                  :label="style.label"
                  :value="style.value"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item>
          <el-button
            type="primary"
            @click="onGenerateLessonPlan"
            :loading="isGenerating"
            icon="MagicStick"
          >
            {{ isGenerating ? '正在生成...' : '智能生成教案' }}
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 灵犀教案 - 展示区域 -->
    <el-card class="display-card" v-if="generatedPlan || isGenerating">
      <template #header>
        <div class="card-header">
          <h3>
            <el-icon><Document /></el-icon> 生成结果
          </h3>
          <el-radio-group
            v-model="planForm.outputFormat"
            size="small"
            v-if="generatedPlan && !isGenerating"
          >
            <el-radio-button label="full">完整版</el-radio-button>
            <el-radio-button label="concise" disabled>速览版</el-radio-button>
            <!-- 速览版待实现 -->
          </el-radio-group>
        </div>
      </template>
      <div v-if="isGenerating" class="loading-placeholder">
        <el-skeleton :rows="10" animated />
      </div>
      <div v-else-if="generatedPlan" class="generated-content" v-html="generatedPlan"></div>
    </el-card>

    <!-- 思辨剧场 - 互动推荐区域 -->
    <el-card class="interactions-card" v-if="generatedPlan && !isGenerating">
      <template #header>
        <div class="card-header">
          <h3>
            <el-icon><ChatDotRound /></el-icon> 思辨剧场 - 互动推荐
          </h3>
          <el-button
            type="primary"
            plain
            @click="fetchRecommendedInteractions"
            :loading="isLoadingInteractions"
            icon="Pointer"
            size="small"
          >
            {{ isLoadingInteractions ? '正在获取...' : '获取互动推荐' }}
          </el-button>
        </div>
      </template>

      <!-- Loading State -->
      <div v-if="isLoadingInteractions" class="loading-placeholder">
        <el-skeleton :rows="3" animated />
      </div>

      <!-- Recommendation List (using el-collapse) -->
      <el-collapse v-else-if="recommendedInteractions.length > 0" accordion>
        <el-collapse-item
          v-for="(item, index) in recommendedInteractions"
          :key="index"
          :name="index"
        >
          <template #title>
            <el-tag
              size="small"
              :type="
                item.type === '提问策略'
                  ? 'primary'
                  : item.type === '小组活动'
                    ? 'success'
                    : 'warning'
              "
              style="margin-right: 8px"
            >
              {{ item.type }}
            </el-tag>
            <span class="interaction-title">{{ item.title }}</span>
          </template>
          <div class="interaction-content" v-html="item.content.replace(/\n/g, '<br/>')"></div>
        </el-collapse-item>
      </el-collapse>

      <!-- Empty State -->
      <el-empty v-else description="暂无推荐，请先点击按钮获取推荐"></el-empty>
    </el-card>

    <!-- 题海星图 -->
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
          <template #default="">
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

      <!-- TODO: Add button/tab for 错题本 -->
    </el-card>

    <!-- 时空走廊 -->
    <el-card class="case-library-card">
      <template #header>
        <div class="card-header">
          <h3>
            <el-icon><Clock /></el-icon> 时空走廊 - 故事与案例
          </h3>
        </div>
      </template>

      <!-- Filters -->
      <div class="filters">
        <el-form :inline="true" :model="caseFilters">
          <el-form-item label="分类">
            <el-select v-model="caseFilters.category" placeholder="选择分类" clearable size="small">
              <el-option v-for="c in caseCategories" :key="c" :label="c" :value="c"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="朝代/时期">
            <el-select v-model="caseFilters.era" placeholder="选择朝代/时期" clearable size="small">
              <el-option v-for="e in eras" :key="e" :label="e" :value="e"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="主题">
            <el-select v-model="caseFilters.theme" placeholder="选择主题" clearable size="small">
              <el-option v-for="t in themes" :key="t" :label="t" :value="t"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="filterCases" icon="Search" size="small"
              >筛选案例</el-button
            >
          </el-form-item>
        </el-form>
      </div>

      <!-- Case List (Cards) -->
      <div class="case-list" v-loading="isCasesLoading">
        <el-card shadow="hover" v-for="item in cases" :key="item.id" class="case-card">
          <template #header>
            <div class="card-header">
              <span>{{ item.title }}</span>
              <el-tag size="small">{{ item.category }}</el-tag>
            </div>
          </template>
          <p class="case-summary">{{ item.summary || '暂无简介...' }}</p>
          <div class="case-footer">
            <el-tag type="info" size="small" v-if="item.era">{{ item.era }}</el-tag>
            <el-tag type="warning" size="small" v-if="item.theme">{{ item.theme }}</el-tag>
            <el-button text type="primary" @click="viewCaseDetails(item.id)">查看详情</el-button>
          </div>
        </el-card>
        <el-empty
          v-if="!isCasesLoading && cases.length === 0"
          description="暂无案例，请调整筛选条件"
        ></el-empty>
      </div>
      <!-- TODO: Add pagination if needed -->
    </el-card>

    <!-- 思辨剧场 - 情景模拟沙盘 (Dialog Placeholder) -->
    <el-dialog
      v-model="showSimulationDialog"
      :title="simulationScenario?.title || '情景模拟'"
      width="60%"
    >
      <div v-if="simulationScenario">
        <p>{{ simulationScenario.description }}</p>
        <!-- TODO: Add interactive elements for the simulation based on scenario data -->
        <el-input
          type="textarea"
          :rows="5"
          placeholder="在此处输入您的模拟操作或回应..."
        ></el-input>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showSimulationDialog = false">关闭</el-button>
          <el-button type="primary" @click="showSimulationDialog = false">提交模拟</el-button>
          <!-- TODO: Add submit logic -->
        </span>
      </template>
    </el-dialog>

    <!-- 最近教案 -->
    <div class="recent-section">
      <div class="section-header">
        <h2>最近教案</h2>
        <el-button text type="primary">查看全部</el-button>
      </div>

      <el-table :data="recentPlans" style="width: 100%">
        <el-table-column prop="title" label="教案名称" min-width="200">
          <template #default="scope">
            <div class="plan-title-cell">
              <el-icon><Document /></el-icon>
              <span>{{ scope.row.title }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="subject" label="学科" width="120"></el-table-column>
        <el-table-column prop="grade" label="年级" width="120"></el-table-column>
        <el-table-column prop="createdAt" label="创建时间" width="180"></el-table-column>
        <el-table-column prop="status" label="状态" width="120">
          <template #default="scope">
            <el-tag :type="scope.row.status === '已完成' ? 'success' : 'warning'">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default>
            <el-button text type="primary" icon="Edit"></el-button>
            <el-button text type="primary" icon="View"></el-button>
            <el-button text type="danger" icon="Delete"></el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 推荐资源 -->
    <div class="resources-section">
      <div class="section-header">
        <h2>推荐资源</h2>
        <el-button text type="primary">更多推荐</el-button>
      </div>

      <div class="resource-cards">
        <el-card class="resource-card" v-for="(resource, index) in resources" :key="index">
          <div class="resource-header">
            <el-avatar :src="resource.avatar"></el-avatar>
            <div class="resource-info">
              <div class="resource-title">{{ resource.title }}</div>
              <div class="resource-author">{{ resource.author }}</div>
            </div>
          </div>
          <div class="resource-content">{{ resource.content }}</div>
          <div class="resource-footer">
            <span class="resource-date">{{ resource.date }}</span>
            <div class="resource-stats">
              <span
                ><el-icon><View /></el-icon> {{ resource.views }}</span
              >
              <span
                ><el-icon><Star /></el-icon> {{ resource.stars }}</span
              >
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<style scoped>
.workshop-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.tool-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.tool-card {
  text-align: center;
  padding: 30px 20px;
  transition: all 0.3s ease;
}

.tool-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.tool-icon {
  margin-bottom: 15px;
}

.tool-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

.tool-desc {
  color: #666;
  margin-bottom: 20px;
  height: 60px;
}

.tool-btn {
  width: 100%;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h2 {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.recent-section {
  margin-bottom: 30px;
}

.plan-title-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.resources-section {
  margin-bottom: 30px;
}

.resource-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.resource-card {
  transition: all 0.3s ease;
}

.resource-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.resource-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  gap: 10px;
}

.resource-info {
  flex: 1;
}

.resource-title {
  font-weight: bold;
  font-size: 16px;
}

.resource-author {
  font-size: 13px;
  color: #666;
}

.resource-content {
  margin-bottom: 15px;
  color: #333;
  height: 80px;
  overflow: hidden;
}

.resource-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #999;
  font-size: 13px;
}

.resource-stats {
  display: flex;
  gap: 15px;
}

.generator-card,
.display-card {
  margin-bottom: 30px;
}

.generator-form .el-select {
  width: 100%; /* Make select boxes fill column */
}

.generated-content {
  line-height: 1.8;
  font-family:
    'KaiTi', 'Times New Roman', serif; /* Example: Use a serif font for better readability */
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 4px;
  background-color: #fdfdfd;
}

.generated-content ::v-deep(strong) {
  /* Style bold text */
  font-weight: bold;
}

.loading-placeholder {
  padding: 20px;
}

/* Style for the display card header */
.display-card .card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.display-card .card-header h3 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 5px;
}

.interactions-card {
  margin-bottom: 30px;
}

.interactions-card .card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.interactions-card .card-header h3 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 5px;
}

.interaction-title {
  font-weight: 500;
}

.interaction-content {
  padding: 10px 15px;
  line-height: 1.7;
  background-color: #fafafa;
  border-radius: 4px;
  white-space: pre-wrap; /* Preserve line breaks */
}

.question-bank-card,
.case-library-card {
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

.case-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  min-height: 100px; /* Ensure loading is visible */
}

.case-card .card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.case-summary {
  color: #666;
  font-size: 14px;
  margin-bottom: 15px;
  min-height: 40px; /* Ensure consistent height */
}

.case-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #f0f0f0;
  padding-top: 10px;
  margin-top: 10px;
}

.case-footer .el-tag {
  margin-right: 5px;
}
</style>

<script lang="ts">
export default {
  data() {
    return {
      tools: [
        {
          title: '灵犀教案',
          description: 'AI智能生成完整教案，包含教学目标、重难点和时间轴',
          icon: 'EditPen',
          color: '#6B42E8',
          buttonText: '生成教案',
          buttonType: 'primary' as const,
        },
        {
          title: '思辨剧场',
          description: '智能推荐互动环节与情景模拟，激发学生思考能力',
          icon: 'ChatDotRound',
          color: '#FF7A5A',
          buttonText: '创建剧场',
          buttonType: 'warning' as const,
        },
        {
          title: '题海星图',
          description: '根据知识点智能匹配题目，支持难度和类型筛选',
          icon: 'Document',
          color: '#54D6FF',
          buttonText: '题库探索',
          buttonType: 'info' as const,
        },
        {
          title: '时空走廊',
          description: '传统文化故事库和跨学科案例，拓展教学视野',
          icon: 'Clock',
          color: '#FFB64D',
          buttonText: '浏览案例',
          buttonType: 'success' as const,
        },
      ],
      recentPlans: [
        {
          title: '《九章算术》与现代数学的联系',
          subject: '数学',
          grade: '初三',
          createdAt: '2023-03-20 14:30',
          status: '已完成',
        },
        {
          title: '春秋战国的历史变革',
          subject: '历史',
          grade: '初二',
          createdAt: '2023-03-18 09:15',
          status: '进行中',
        },
        {
          title: '光的折射与日常生活',
          subject: '物理',
          grade: '初三',
          createdAt: '2023-03-15 16:40',
          status: '已完成',
        },
        {
          title: '诗词中的意象分析',
          subject: '语文',
          grade: '高一',
          createdAt: '2023-03-10 10:20',
          status: '已完成',
        },
      ],
      resources: [
        {
          title: '如何让数学课更有趣',
          author: '李明 · 特级教师',
          content: '分享10种让学生爱上数学的互动教学方法，通过游戏化和生活实例激发学习兴趣...',
          date: '2023-03-15',
          views: 2341,
          stars: 189,
          avatar: '/src/assets/avatar1.jpg',
        },
        {
          title: '传统文化融入语文教学',
          author: '王华 · 教研组长',
          content: '详解如何将传统节日、古代礼仪等文化元素自然融入语文课堂，增强文化认同感...',
          date: '2023-03-12',
          views: 1892,
          stars: 156,
          avatar: '/src/assets/avatar2.jpg',
        },
        {
          title: '物理实验创新设计指南',
          author: '张科 · 学科带头人',
          content: '使用简单材料设计有趣的物理实验，让抽象概念变得直观可感，提升教学效果...',
          date: '2023-03-08',
          views: 1654,
          stars: 142,
          avatar: '/src/assets/avatar3.jpg',
        },
      ],
    };
  },
};
</script>
