<template>
  <a-layout style="height: 100vh">
    <a-layout-sider width="200" theme="light">
      <a-menu
        mode="inline"
        :selected-keys="[selectedKey]"
        @select="onSelect"
        style="height: 100%; border-right: 0"
      >
        <a-menu-item key="1">
          <template #icon>
            <form-outlined />
          </template>
          智能教案生成
        </a-menu-item>
        <a-menu-item key="2">
          <template #icon>
            <interaction-outlined />
          </template>
          互动环节设计
        </a-menu-item>
        <a-menu-item key="3">
          <template #icon>
            <book-outlined />
          </template>
          教学资源库
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout-content style="padding: 24px; min-height: 280px">
      <lesson-plan-generator v-if="selectedKey === '1'" />
      <interactive-activity-designer v-if="selectedKey === '2'" />
      <teaching-resource-library v-if="selectedKey === '3'" />
    </a-layout-content>
  </a-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { FormOutlined, BookOutlined, InteractionOutlined } from '@ant-design/icons-vue';
import LessonPlanGenerator from './workbench/LessonPlanGenerator.vue';
import InteractiveActivityDesigner from './workbench/InteractiveActivityDesigner.vue';
import TeachingResourceLibrary from './workbench/TeachingResourceLibrary.vue';

const selectedKey = ref('1');

const onSelect = (e: { key: string }) => {
  selectedKey.value = e.key;
};
</script>
