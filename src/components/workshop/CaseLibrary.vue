<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import {
  getCases,
  getDynasties,
  getThemes,
  getDisciplines,
  generateCase,
  generateStory,
  getStories,
  getStoryDetail,
} from '@/api';
import type {
  CaseItem,
  CaseFilters,
  DynastyInfo,
  ThemeCategory,
  DisciplineCategory,
  GenerateStoryRequest,
  GenerateCaseRequest,
  StoryItem,
  StoryFilters,
} from '@/api';
import {
  StoryFilters as StoryFilterComp,
  CaseFilters as CaseFilterComp,
  GenerateDialog,
  ContentList,
  StoryCard,
  CaseCard,
  StoryDetail,
  CaseDetail,
} from './case';

// 分类数据
const dynasties = ref<DynastyInfo[]>([]);
const themes = ref<ThemeCategory[]>([]);
const disciplines = ref<DisciplineCategory[]>([]);

// 故事相关状态
const stories = ref<StoryItem[]>([]);
const isStoriesLoading = ref<boolean>(false);

// 案例相关状态
const cases = ref<CaseItem[]>([]);
const isCasesLoading = ref<boolean>(false);

// 生成对话框状态
const showGenerateDialog = ref(false);
const dialogType = ref<'story' | 'case'>('story');

// 添加详情对话框状态
const showStoryDetail = ref(false);
const showCaseDetail = ref(false);
const currentStory = ref<StoryItem | null>(null);
const currentCase = ref<CaseItem | null>(null);

// 加载分类数据
const loadCategories = async () => {
  try {
    const [dynastyData, themeData, disciplineData] = await Promise.all([
      getDynasties(),
      getThemes(),
      getDisciplines(),
    ]);
    dynasties.value = dynastyData;
    themes.value = themeData;
    disciplines.value = disciplineData;
  } catch (error) {
    console.error('Error loading categories:', error);
    ElMessage.error('加载分类数据失败');
  }
};

// 故事列表处理
const handleStoryFilter = async (filters: StoryFilters) => {
  isStoriesLoading.value = true;
  try {
    stories.value = await getStories(filters);
  } catch (error) {
    console.error('Error filtering stories:', error);
    ElMessage.error('获取故事失败，请稍后重试');
    stories.value = [];
  } finally {
    isStoriesLoading.value = false;
  }
};

// 案例列表处理
const handleCaseFilter = async (filters: CaseFilters) => {
  isCasesLoading.value = true;
  try {
    cases.value = await getCases(filters);
  } catch (error) {
    console.error('Error filtering cases:', error);
    ElMessage.error('获取案例失败，请稍后重试');
    cases.value = [];
  } finally {
    isCasesLoading.value = false;
  }
};

// 生成内容处理
const openGenerateDialog = (type: 'story' | 'case') => {
  dialogType.value = type;
  showGenerateDialog.value = true;
};

const handleGenerate = async (
  type: 'story' | 'case',
  data: GenerateStoryRequest | GenerateCaseRequest,
) => {
  try {
    if (type === 'story') {
      await generateStory(data as GenerateStoryRequest);
      await handleStoryFilter({});
      ElMessage.success('故事生成成功');
    } else {
      await generateCase(data as GenerateCaseRequest);
      await handleCaseFilter({});
      ElMessage.success('案例生成成功');
    }
    showGenerateDialog.value = false;
  } catch (error) {
    console.error('Generation error:', error);
    ElMessage.error('生成失败，请重试');
  }
};

// 添加详情对话框处理函数
const handleStoryDetail = (story: StoryItem) => {
  currentStory.value = story;
  showStoryDetail.value = true;
};

const handleCaseDetail = (case_: CaseItem) => {
  currentCase.value = case_;
  showCaseDetail.value = true;
};

// 查看关联故事
const handleViewStory = async (storyId: string) => {
  try {
    const story = await getStoryDetail(storyId);
    currentStory.value = story;
    showCaseDetail.value = false;
    showStoryDetail.value = true;
  } catch (error) {
    console.error('Error loading story:', error);
    ElMessage.error('加载故事失败');
  }
};

// 初始化
onMounted(() => {
  loadCategories();
  handleStoryFilter({});
  handleCaseFilter({});
});
</script>

<template>
  <el-card class="case-library-card">
    <template #header>
      <div class="card-header">
        <h3>时空走廊 - 故事与案例</h3>
        <div class="header-actions">
          <el-button type="primary" @click="openGenerateDialog('story')">生成故事</el-button>
          <el-button type="success" @click="openGenerateDialog('case')">生成案例</el-button>
        </div>
      </div>
    </template>

    <el-tabs>
      <el-tab-pane label="传统故事">
        <story-filter-comp :dynasties="dynasties" :themes="themes" @filter="handleStoryFilter" />
        <content-list :loading="isStoriesLoading" :isEmpty="stories.length === 0">
          <story-card
            v-for="story in stories"
            :key="story.id"
            :story="story"
            @detail="handleStoryDetail"
          />
        </content-list>
      </el-tab-pane>

      <el-tab-pane label="教学案例">
        <case-filter-comp :disciplines="disciplines" @filter="handleCaseFilter" />
        <content-list :loading="isCasesLoading" :isEmpty="cases.length === 0">
          <case-card
            v-for="case_ in cases"
            :key="case_.id"
            :case_="case_"
            @detail="handleCaseDetail"
          />
        </content-list>
      </el-tab-pane>
    </el-tabs>

    <generate-dialog
      v-model:visible="showGenerateDialog"
      :type="dialogType"
      :dynasties="dynasties"
      :themes="themes"
      :disciplines="disciplines"
      @generate="handleGenerate"
    />

    <!-- 故事详情对话框 -->
    <story-detail v-model:visible="showStoryDetail" :story="currentStory" />

    <!-- 案例详情对话框 -->
    <case-detail
      v-model:visible="showCaseDetail"
      :case_="currentCase"
      @view-story="handleViewStory"
    />
  </el-card>
</template>

<style scoped>
.case-library-card {
  :deep(.el-card__body) {
    padding: 20px;
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  h3 {
    margin: 0;
  }
}

/* 调整标签页样式 */
:deep(.el-tabs__content) {
  padding-top: 20px;
}

/* 确保对话框显示在最上层 */
:deep(.el-dialog) {
  margin-top: 5vh !important;
}

:deep(.el-dialog__wrapper) {
  z-index: 2000;
}
</style>
