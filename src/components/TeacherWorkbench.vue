<template>
  <el-container class="workbench-layout">
    <el-aside width="200px">
      <el-menu
        mode="vertical"
        :default-active="selectedKey"
        @select="onSelect"
        style="height: 100%"
      >
        <el-menu-item v-for="item in menuItems" :key="item.key" :index="item.key">
          <el-icon>
            <component :is="item.icon" />
          </el-icon>
          <span>{{ item.title }}</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-main class="workbench-content">
      <component :is="currentComponent" v-if="currentComponent" />
      <div v-else class="loading">加载中...</div>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed, defineAsyncComponent } from 'vue';
import { Document, Collection, ChatLineRound, Picture } from '@element-plus/icons-vue';

// 定义菜单和组件映射
const menuItems = [
  {
    key: '1',
    title: '智能教案生成',
    icon: Document,
    component: defineAsyncComponent(() => import('./workbench/LessonPlanGenerator.vue')),
  },
  {
    key: '2',
    title: '互动环节设计',
    icon: ChatLineRound,
    component: defineAsyncComponent(() => import('./workbench/InteractiveActivityDesigner.vue')),
  },
  {
    key: '3',
    title: '教学资源库',
    icon: Collection,
    component: defineAsyncComponent(() => import('./workbench/TeachingResourceLibrary.vue')),
  },
  {
    key: '4',
    title: '艺术风格转化',
    icon: Picture,
    component: defineAsyncComponent(() => import('./workbench/ArtStyleConverter.vue')),
  },
];

const selectedKey = ref('1');

// 根据selectedKey计算当前应该显示的组件
const currentComponent = computed(() => {
  const selectedItem = menuItems.find((item) => item.key === selectedKey.value);
  return (selectedItem || menuItems[0]).component;
});

// 菜单选择处理函数
const onSelect = (key: string) => {
  selectedKey.value = key;
};
</script>

<style scoped>
.workbench-layout {
  height: 100%;
  overflow: hidden;
}

.workbench-content {
  padding: 24px;
  overflow: auto;
  height: 100%;
}

.loading {
  text-align: center;
  padding: 20px;
  font-size: 16px;
  color: #999;
}
</style>
