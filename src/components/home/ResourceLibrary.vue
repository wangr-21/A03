<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import type { TabsPaneContext } from 'element-plus';
import type { Resource } from '@/api';

// Props定义
const props = defineProps<{
  resources: Resource[];
  loading: boolean;
  activeTab: string;
  selectedSubject: string;
  selectedGrade: string;
}>();

// Emits
const emit = defineEmits<{
  filtersChange: [filters: { tab: string; subject: string; grade: string }];
}>();

// 本地状态
const localActiveTab = ref(props.activeTab);
const localSelectedSubject = ref(props.selectedSubject);
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
  () => props.selectedSubject,
  (newVal) => {
    localSelectedSubject.value = newVal;
  },
);

watch(
  () => props.selectedGrade,
  (newVal) => {
    localSelectedGrade.value = newVal;
  },
);

// 可选项
const subjects: string[] = [
  '语文',
  '数学',
  '英语',
  '物理',
  '化学',
  '历史',
  '地理',
  '生物',
  '政治',
  '党建',
];

const grades: string[] = [
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
];

// 过滤资源
const filteredResources = computed<Resource[]>(() => {
  return props.resources.filter((resource) => {
    const typeMatch = localActiveTab.value === 'all' || resource.type === localActiveTab.value;
    const subjectMatch =
      !localSelectedSubject.value || resource.subject === localSelectedSubject.value;
    const gradeMatch = !localSelectedGrade.value || resource.grade === localSelectedGrade.value;
    return typeMatch && subjectMatch && gradeMatch;
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
    subject: localSelectedSubject.value,
    grade: localSelectedGrade.value,
  });
};

// 应用过滤器
const applyFilters = (): void => {
  resourceCurrentPage.value = 1;
  emit('filtersChange', {
    tab: localActiveTab.value,
    subject: localSelectedSubject.value,
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
            <el-tab-pane label="电子课本" name="textbook"></el-tab-pane>
            <el-tab-pane label="党建专题" name="party"></el-tab-pane>
          </el-tabs>
          <div class="filter-controls">
            <el-select
              v-model="localSelectedSubject"
              placeholder="选择学科"
              size="small"
              clearable
              @change="applyFilters"
            >
              <el-option
                v-for="subject in subjects"
                :key="subject"
                :label="subject"
                :value="subject"
              ></el-option>
            </el-select>
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

    <div class="resource-grid" v-loading="loading" element-loading-text="加载资源中...">
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
            <span>{{ resource.subject }}</span> | <span>{{ resource.grade }}</span>
          </div>
          <el-button text type="primary" @click="viewResource(resource.id)">开始阅读</el-button>
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
      description="暂无匹配资源"
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
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding: 15px 20px 0;
}

.card-header h3 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin: 0;
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
  margin-bottom: 15px;
}

/* 响应式调整过滤器 */
@media (max-width: 768px) {
  .library-filters {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .filter-controls {
    margin-top: 10px;
    width: 100%;
  }

  .filter-controls .el-select {
    width: 100%;
    margin-bottom: 10px;
  }
}

.filter-controls {
  display: flex;
  gap: 15px;
}

.resource-grid {
  display: flex;
  flex-direction: column;
  gap: 15px;
  min-height: 200px;
  padding: 0 20px 20px;
}

.resource-card {
  display: flex;
  align-items: center;
  padding: 15px;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  transition: all 0.3s ease;
  background-color: #fff;
}

.resource-card:hover {
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}

/* 资源卡片响应式调整 */
@media (max-width: 480px) {
  .resource-card {
    flex-direction: column;
    align-items: flex-start;
  }

  .resource-cover {
    width: 100%;
    height: 200px;
    margin-right: 0;
    margin-bottom: 15px;
  }
}

.resource-cover {
  width: 120px;
  height: 160px;
  overflow: hidden;
  border-radius: 6px;
  margin-right: 20px;
  position: relative;
}

.resource-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.party-tag {
  position: absolute;
  right: 5px;
  top: 5px;
}

.resource-info {
  flex: 1;
}

.resource-info h4 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.resource-meta {
  font-size: 14px;
  color: #909399;
  margin-bottom: 10px;
}

.resource-info .el-button {
  margin-top: 5px;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>
