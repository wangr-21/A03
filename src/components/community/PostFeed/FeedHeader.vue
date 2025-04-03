<script setup lang="ts">
import { ref, watch } from 'vue';

const props = defineProps<{
  activeTab: string;
  searchQuery: string;
}>();

const emit = defineEmits(['tab-change', 'search']);

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
}

.feed-filters .el-tabs {
  margin-bottom: -1px; /* 与底部边框对齐 */
}

.search-input {
  width: 250px;
}

@media (max-width: 768px) {
  .feed-filters {
    flex-direction: column;
  }

  .search-input {
    margin-top: 10px;
    width: 100%;
  }
}
</style>
