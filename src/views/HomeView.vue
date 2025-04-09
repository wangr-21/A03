<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getResources, getSidebarData } from '@/api';
import { ElMessage } from 'element-plus';
import type { Resource } from '@/api';
import {
  StatsCards,
  ContactList,
  ShowcaseCarousel,
  HotspotCard,
  ResourceLibrary,
  KnowledgeGraph,
  HomeHotTopics,
} from '@/components/home';

// 资源库相关数据
const allResources = ref<Resource[]>([]);
const resourcesLoading = ref<boolean>(false);
const activeLibraryTab = ref<string>('all');
// const selectedSubject = ref<string>(''); // 移除学科状态
const selectedGrade = ref<string>('');

// 热门话题
const hotTags = ref<string[]>([]);

// 获取资源数据
const fetchResources = async (filters?: {
  type?: string;
  // subject?: string; // 移除学科过滤
  grade?: string;
}): Promise<void> => {
  resourcesLoading.value = true;
  console.log('Fetching resources with filters:', filters);

  try {
    const response = await getResources({
      type: filters?.type === 'all' ? undefined : filters?.type,
      // subject: filters?.subject,
      grade: filters?.grade,
    });

    if (response.success) {
      allResources.value = response.data.resources;
    } else {
      throw new Error('Failed to fetch resources');
    }
  } catch (error) {
    console.error('Error fetching resources:', error);
    ElMessage.error('获取资源失败，请稍后重试');
  } finally {
    resourcesLoading.value = false;
  }
};

// 获取热门话题数据
const fetchHotTags = async () => {
  try {
    const data = await getSidebarData();
    hotTags.value = data.hotTags;
  } catch (error) {
    console.error('Error fetching hot tags:', error);
  }
};

// 过滤资源变化处理
const handleFiltersChange = (filters: { tab: string; grade: string }) => { // 移除学科属性
  activeLibraryTab.value = filters.tab;
  // selectedSubject.value = filters.subject; // 移除学科更新
  selectedGrade.value = filters.grade;

  fetchResources({
    type: filters.tab,
    // subject: filters.subject,
    grade: filters.grade,
  });
};

onMounted(() => {
  fetchResources();
  fetchHotTags();
});
</script>

<template>
  <div class="home-container">
    <div class="page-header">
      <h1 class="page-title">启智学堂</h1>
    </div>

    <!-- 热门话题区域 -->
    <HomeHotTopics :tags="hotTags" class="hot-topics-section" />

    <!-- 统计卡片区域 -->
    <StatsCards />

    <!-- 联系人区域 -->
    <ContactList />

    <!-- 流光展台区域 -->
    <el-row :gutter="20" class="showcase-area">
      <el-col :span="16">
        <ShowcaseCarousel />
      </el-col>
      <el-col :span="8">
        <HotspotCard />
      </el-col>
    </el-row>

    <!-- 智汇文库区域 -->
    <ResourceLibrary
      :resources="allResources"
      :loading="resourcesLoading"
      :active-tab="activeLibraryTab"
      :selected-grade="selectedGrade"
      @filters-change="handleFiltersChange"
    />

    <!-- 学科星云区域 -->
    <KnowledgeGraph />
  </div>
</template>

<style scoped>
.home-container {
  padding: 20px;
  min-height: 100%;
}

.page-header {
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.hot-topics-section {
  margin-bottom: 20px;
}

.showcase-area {
  margin-bottom: 30px;
}

/* 响应式调整展示区域 */
@media (max-width: 991px) {
  .el-col[class*='el-col-'] {
    width: 100%;
    margin-bottom: 20px;
  }
}
</style>
