<script setup lang="ts">
import { ref, watch } from 'vue';

const props = defineProps<{
  activeTab: string;
  searchQuery: string;
}>();

const emit = defineEmits<{
  'tab-change': [activeTab: string];
  search: [searchQuery: string];
}>();

const localActiveTab = ref(props.activeTab);
const localSearchQuery = ref(props.searchQuery);

// 监听父组件传入的值
watch(
  () => props.activeTab,
  (newVal) => {
    localActiveTab.value = newVal;
  },
);

watch(
  () => props.searchQuery,
  (newVal) => {
    localSearchQuery.value = newVal;
  },
);

// 标签切换处理
const handleTabChange = () => {
  emit('tab-change', localActiveTab.value);
};

// 搜索处理
const handleSearch = () => {
  emit('search', localSearchQuery.value);
};

// 清空搜索
const handleClear = () => {
  localSearchQuery.value = '';
  emit('search', '');
};
</script>

<template>
  <div class="feed-filters">
    <el-tabs v-model="localActiveTab" @tab-change="handleTabChange">
      <el-tab-pane label="最新发布" name="latest"></el-tab-pane>
      <el-tab-pane label="热门讨论" name="hot"></el-tab-pane>
      <el-tab-pane label="精华推荐" name="featured"></el-tab-pane>
    </el-tabs>
    <el-input
      placeholder="搜索帖子内容或标签"
      prefix-icon="Search"
      v-model="localSearchQuery"
      size="small"
      class="search-input"
      @keyup.enter="handleSearch"
      clearable
      @clear="handleClear"
    >
      <template #append>
        <el-button icon="Search" @click="handleSearch"></el-button>
      </template>
    </el-input>
  </div>
</template>

<style scoped>
.feed-filters {
  background-color: #fff;
  padding: 5px 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  flex-wrap: wrap; /* 允许内容在需要时换行 */
}

.feed-filters .el-tabs {
  margin-bottom: -1px; /* 与底部边框对齐 */
  min-width: 300px; /* 确保标签栏有足够的最小宽度 */
  flex: 1; /* 允许标签栏伸展 */
  overflow-x: auto; /* 在小屏幕上允许滚动 */
}

.feed-filters .el-tabs :deep(.el-tabs__header) {
  margin: 0;
}

.feed-filters .el-tabs :deep(.el-tabs__nav-wrap::after) {
  height: 1px; /* 减小底部线条高度 */
}

.search-input {
  width: 250px;
  margin-left: 10px;
}

/* 宽屏幕断点 */
@media (max-width: 1200px) {
  .feed-filters {
    padding: 5px 10px;
  }

  .search-input {
    width: 200px;
  }
}

/* 平板断点 */
@media (max-width: 992px) {
  .feed-filters .el-tabs {
    min-width: 250px;
  }

  .search-input {
    width: 180px;
  }
}

/* 移动端断点 */
@media (max-width: 768px) {
  .feed-filters {
    flex-direction: column;
    padding: 10px;
  }

  .feed-filters .el-tabs {
    width: 100%;
    margin-bottom: 10px;
  }

  .search-input {
    margin-top: 5px;
    margin-left: 0;
    width: 100%;
  }
}

/* 小型移动设备断点 */
@media (max-width: 480px) {
  .feed-filters {
    padding: 8px;
  }

  .feed-filters .el-tabs :deep(.el-tabs__item) {
    padding: 0 12px; /* 减小标签之间的间距 */
  }
}
</style>
