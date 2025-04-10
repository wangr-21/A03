<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
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

// 本地状态 - 确保默认值为'textbook'
const localActiveTab = ref('textbook'); // 直接设置默认值为textbook
const localSelectedGrade = ref(props.selectedGrade);
const resourcePageSize = ref<number>(5);
const resourceCurrentPage = ref<number>(1);

// 组件挂载时确保选中美术课本
onMounted(() => {
  // 确保默认选中美术课本
  if (localActiveTab.value !== 'textbook') {
    localActiveTab.value = 'textbook';
    emit('filtersChange', {
      tab: 'textbook',
      grade: localSelectedGrade.value,
    });
  }
});

// 监听props变化，更新本地状态
watch(
  () => props.activeTab,
  (newVal) => {
    if (newVal) {
      // 如果传入的是已删除的选项卡，则默认选择textbook
      localActiveTab.value = (newVal === 'all' || newVal === 'reference') ? 'textbook' : newVal;
    } else {
      // 如果没有传入值，确保默认为textbook
      localActiveTab.value = 'textbook';
    }
  },
  { immediate: true } // 立即执行一次
);

watch(
  () => props.selectedGrade,
  (newVal) => {
    localSelectedGrade.value = newVal;
  },
);

// 可选项
const grades: string[] = ['初一', '初二', '初三'];

// 控制年级选择器显示
const showGradeSelector = computed(() => {
  return localActiveTab.value === 'textbook';
});

// 过滤资源
const filteredResources = computed<Resource[]>(() => {
  return props.resources.filter((resource) => {
    // 修改过滤逻辑，不再支持'all'选项
    const typeMatch = resource.type === localActiveTab.value;
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
const viewResource = (resource: Resource): void => {
  console.log('View resource:', resource.id);

  // 如果有PDF路径，则打开PDF
  if (resource.pdfPath) {
    // 方法1: 使用window.open打开PDF (适用于web环境)
    window.open(resource.pdfPath, '_blank');

    // 方法2: 如果是Electron应用，可以使用Electron的shell.openExternal
    // 需要先导入: import { shell } from 'electron'
    // shell.openExternal(resource.pdfPath);
  }
};

// 打开党建网站
const openPartyWebsite = () => {
  window.open('https://www.12371.cn/special/xz/', '_blank');
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
            <el-tab-pane label="美术课本" name="textbook"></el-tab-pane>
            <el-tab-pane label="党建专题" name="party"></el-tab-pane>
          </el-tabs>
          <div class="filter-controls">
            <!-- 修改年级选择器样式 -->
            <el-select
              v-if="showGradeSelector"
              v-model="localSelectedGrade"
              placeholder="请选择年级"
              size="default"
              clearable
              class="grade-selector"
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

    <!-- 美术课本内容 -->
    <div v-if="localActiveTab === 'textbook'" class="resource-grid" v-loading="loading" element-loading-text="加载资源中...">
      <el-card
        class="resource-card"
        v-for="resource in paginatedResources"
        :key="resource.id"
        shadow="hover"
      >
        <div class="resource-cover">
          <img :src="resource.cover" :alt="resource.title" />
        </div>
        <div class="resource-info">
          <h4>{{ resource.title }}</h4>
          <div class="resource-meta">
            <span>{{ resource.grade }}</span>
          </div>
          <el-button text type="primary" @click="viewResource(resource)">查看资源</el-button>
        </div>
      </el-card>
    </div>

    <!-- 党建专题内容 -->
    <div v-if="localActiveTab === 'party'" class="party-content">
      <el-button
        :type="localActiveTab === 'party' ? 'danger' : 'default'"
        size="large"
        class="party-button"
        @click="openPartyWebsite"
      >
        <el-icon class="party-icon"><Link /></el-icon>
        访问党建专题网站
      </el-button>
    </div>

    <!-- 分页 -->
    <div class="pagination" v-if="localActiveTab === 'textbook' && filteredResources.length > 0">
      <el-pagination
        background
        layout="prev, pager, next"
        :total="filteredResources.length"
        :page-size="resourcePageSize"
        v-model:current-page="resourceCurrentPage"
        @current-change="handleResourcePageChange"
      ></el-pagination>
    </div>

    <!-- 空状态 -->
    <el-empty
      v-if="localActiveTab === 'textbook' && !loading && filteredResources.length === 0"
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

/* 添加年级选择器样式 */
.grade-selector {
  width: 240px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}

:deep(.grade-selector .el-input__wrapper) {
  border: none;
  box-shadow: none !important;
}

:deep(.grade-selector .el-input__inner) {
  color: #606266;
  font-size: 14px;
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

/* 党建专题样式 */
.party-content {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 20px;
  min-height: 200px;  /* 减小最小高度 */
}

.party-button {
  width: 60%;  /* 减小宽度 */
  height: 80px;  /* 减小高度 */
  font-size: 20px;  /* 减小字体大小 */
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;  /* 减小图标和文字的间距 */
  border-radius: 6px;  /* 稍微减小圆角 */
  transition: all 0.3s ease;
}

.party-icon {
  font-size: 22px;  /* 减小图标大小 */
}
.party-button.el-button--danger {
  background-color: #c5281c;
  border-color: #c5281c;
  box-shadow: 0 4px 12px rgba(197, 40, 28, 0.3);
}

.party-button.el-button--default {
  background-color: #ffffff;
  border-color: #dcdfe6;
  color: #606266;
}

.party-button:hover {
  transform: translateY(-5px);
}

.party-button.el-button--danger:hover {
  box-shadow: 0 8px 20px rgba(197, 40, 28, 0.4);
  background-color: #d92d20;
  border-color: #d92d20;
}

.party-button.el-button--default:hover {
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
  border-color: #c0c4cc;
}

.party-icon {
  font-size: 28px;
}
</style>
