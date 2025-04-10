<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import type { TabsPaneContext } from 'element-plus';
import type { Resource } from '@/api';

// Props定义
const props = defineProps<{
  resources: Resource[];
  loading: boolean;
  activeTab: string;
  selectedGrade: string;
}>();

// Emits
const emit = defineEmits<{
  filtersChange: [filters: { tab: string; grade: string }];
}>();

// 本地状态
const localActiveTab = ref(props.activeTab);
const localSelectedGrade = ref(props.selectedGrade);
const resourcePageSize = ref<number>(5);
const resourceCurrentPage = ref<number>(1);

// 监听props变化，更新本地状态
watch(
  () => props.activeTab,
  (newVal) => {
    localActiveTab.value = newVal;
  },
);

watch(
  () => props.selectedGrade,
  (newVal) => {
    localSelectedGrade.value = newVal;
  },
);

// 可选项
const grades: string[] = ['初一', '初二', '初三'];

// 过滤资源
const filteredResources = computed<Resource[]>(() => {
  return props.resources.filter((resource) => {
    const typeMatch = localActiveTab.value === 'all' || resource.type === localActiveTab.value;
    const gradeMatch = !localSelectedGrade.value || resource.grade === localSelectedGrade.value;
    return typeMatch && gradeMatch;
  });
});

// 分页资源
const paginatedResources = computed<Resource[]>(() => {
  const start = (resourceCurrentPage.value - 1) * resourcePageSize.value;
  const end = start + resourcePageSize.value;
  return filteredResources.value.slice(start, end);
});

// 处理标签点击
const handleTabClick = (
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  tab: TabsPaneContext,
): void => {
  resourceCurrentPage.value = 1; // 切换标签时重置页码
  emit('filtersChange', {
    tab: localActiveTab.value,
    grade: localSelectedGrade.value,
  });
};

// 应用过滤器
const applyFilters = (): void => {
  resourceCurrentPage.value = 1;
  emit('filtersChange', {
    tab: localActiveTab.value,
    grade: localSelectedGrade.value,
  });
};

// 处理页码变化
const handleResourcePageChange = (page: number): void => {
  resourceCurrentPage.value = page;
};

// 查看资源详情
const viewResource = (id: number): void => {
  console.log('View resource:', id);
};
</script>

<template>
  <el-card class="resource-library-card">
    <template #header>
      <div class="card-header">
        <h3>
          <el-icon><Reading /></el-icon> 智汇文库
        </h3>
        <div class="library-filters">
          <el-tabs v-model="localActiveTab" @tab-click="handleTabClick">
            <el-tab-pane label="全部资源" name="all"></el-tab-pane>
            <el-tab-pane label="教材课件" name="textbook"></el-tab-pane>
            <el-tab-pane label="教学参考" name="reference"></el-tab-pane>
            <el-tab-pane label="党建专题" name="party"></el-tab-pane>
          </el-tabs>
          <div class="filter-controls">
            <el-select
              v-model="localSelectedGrade"
              placeholder="选择年级"
              size="small"
              clearable
              @change="applyFilters"
            >
              <el-option
                v-for="grade in grades"
                :key="grade"
                :label="grade"
                :value="grade"
              ></el-option>
            </el-select>
          </div>
        </div>
      </div>
    </template>

    <div class="resource-grid" v-loading="loading" element-loading-text="加载美术资源中...">
      <el-card
        class="resource-card"
        v-for="resource in paginatedResources"
        :key="resource.id"
        shadow="hover"
      >
        <div class="resource-cover">
          <img :src="resource.cover" :alt="resource.title" />
          <el-tag v-if="resource.type === 'party'" type="danger" class="party-tag">党建</el-tag>
        </div>
        <div class="resource-info">
          <h4>{{ resource.title }}</h4>
          <div class="resource-meta">
            <span>{{ resource.grade }}</span>
          </div>
          <el-button text type="primary" @click="viewResource(resource.id)">查看资源</el-button>
        </div>
      </el-card>
    </div>

    <div class="pagination" v-if="filteredResources.length > 0">
      <el-pagination
        background
        layout="prev, pager, next"
        :total="filteredResources.length"
        :page-size="resourcePageSize"
        v-model:current-page="resourceCurrentPage"
        @current-change="handleResourcePageChange"
      ></el-pagination>
    </div>

    <el-empty
      v-if="!loading && filteredResources.length === 0"
      description="暂无匹配的美术资源"
    ></el-empty>
  </el-card>
</template>

<style scoped>
.resource-library-card {
  margin-bottom: 30px;
  border-radius: 8px;
  overflow: hidden;
}

.card-header {
  padding: 15px 20px 0;
}

.card-header h3 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin: 0 0 15px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-header h3 .el-icon {
  color: #7353e5;
}

.library-filters {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

.library-filters .el-tabs {
  margin-bottom: 10px;
}

.filter-controls {
  display: flex;
  gap: 10px;
  margin-left: auto;
}

.resource-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
  padding: 20px;
  min-height: 200px;
}

.resource-card {
  border-radius: 8px;
  overflow: hidden;
}

.resource-cover {
  position: relative;
  width: 100%;
  padding-top: 140%;
  background-color: #f5f7fa;
}

.resource-cover img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.party-tag {
  position: absolute;
  top: 10px;
  right: 10px;
}

.resource-info {
  padding: 15px;
}

.resource-info h4 {
  font-size: 16px;
  margin: 0 0 10px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.resource-meta {
  font-size: 12px;
  color: #909399;
  margin-bottom: 10px;
}

.resource-info .el-button {
  padding: 0;
}

.pagination {
  margin-top: 20px;
  padding: 20px;
  display: flex;
  justify-content: center;
}
</style>
