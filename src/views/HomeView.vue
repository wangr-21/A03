<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getResources } from '@/api';
import { ElMessage } from 'element-plus';
import type { Resource } from '@/api';

// 导入拆分后的组件
import StatsCards from '@/components/home/StatsCards.vue';
import OverviewChart from '@/components/home/OverviewChart.vue';
import ContactList from '@/components/home/ContactList.vue';
import ShowcaseCarousel from '@/components/home/Showcase/ShowcaseCarousel.vue';
import HotspotCard from '@/components/home/Showcase/HotspotCard.vue';
import ResourceLibrary from '@/components/home/ResourceLibrary.vue';
import KnowledgeGraph from '@/components/home/KnowledgeGraph.vue';

// 资源库相关数据
const allResources = ref<Resource[]>([]);
const resourcesLoading = ref<boolean>(false);
const activeLibraryTab = ref<string>('all');
const selectedSubject = ref<string>('');
const selectedGrade = ref<string>('');

// 获取资源数据
const fetchResources = async (filters?: {
  type?: string;
  subject?: string;
  grade?: string;
}): Promise<void> => {
  resourcesLoading.value = true;
  console.log('Fetching resources with filters:', filters);

  try {
    const response = await getResources({
      type: filters?.type === 'all' ? undefined : filters?.type,
      subject: filters?.subject,
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

// 过滤资源变化处理
const handleFiltersChange = (filters: { tab: string; subject: string; grade: string }) => {
  activeLibraryTab.value = filters.tab;
  selectedSubject.value = filters.subject;
  selectedGrade.value = filters.grade;

  fetchResources({
    type: filters.tab,
    subject: filters.subject,
    grade: filters.grade,
  });
};

onMounted(() => {
  fetchResources();
});
</script>

<template>
  <div class="home-container">
    <div class="page-header">
      <h1 class="page-title">启智学堂</h1>
    </div>

    <!-- 概览图表区域 -->
    <OverviewChart />

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
      :selected-subject="selectedSubject"
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
