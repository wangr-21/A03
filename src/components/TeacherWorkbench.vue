<template>
  <a-layout class="workbench-layout">
    <a-layout-sider width="200" theme="light">
      <a-menu mode="inline" :selected-keys="[selectedKey]" @select="onSelect" style="height: 100%">
        <a-menu-item v-for="item in menuItems" :key="item.key">
          <template #icon>
            <component :is="item.icon" />
          </template>
          {{ item.title }}
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout-content class="workbench-content">
      <component :is="currentComponent" v-if="currentComponent" />
      <div v-else class="loading">加载中...</div>
    </a-layout-content>
  </a-layout>
</template>

<script setup lang="ts">
import { ref, computed, defineAsyncComponent, DefineComponent, FunctionalComponent } from 'vue';
import {
  FormOutlined,
  BookOutlined,
  InteractionOutlined,
  PictureOutlined,
} from '@ant-design/icons-vue';

// 定义菜单和组件映射
const menuItems = [
  {
    key: '1',
    title: '智能教案生成',
    icon: FormOutlined,
    component: defineAsyncComponent(() => import('./workbench/LessonPlanGenerator.vue')),
  },
  {
    key: '2',
    title: '互动环节设计',
    icon: InteractionOutlined,
    component: defineAsyncComponent(() => import('./workbench/InteractiveActivityDesigner.vue')),
  },
  {
    key: '3',
    title: '教学资源库',
    icon: BookOutlined,
    component: defineAsyncComponent(() => import('./workbench/TeachingResourceLibrary.vue')),
  },
  {
    key: '4',
    title: '艺术风格转化',
    icon: PictureOutlined,
    component: defineAsyncComponent(() => import('./workbench/ArtStyleConverter.vue')),
  },
] as {
  key: string;
  title: string;
  icon: FunctionalComponent;
  component: DefineComponent;
}[];

const selectedKey = ref<string>('1');

// 根据selectedKey计算当前应该显示的组件
const currentComponent = computed(() => {
  const selectedItem = menuItems.find((item) => item.key === selectedKey.value);
  return (selectedItem || menuItems[0]).component;
});

// 菜单选择处理函数
const onSelect = (e: { key: string }) => {
  selectedKey.value = e.key;
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
