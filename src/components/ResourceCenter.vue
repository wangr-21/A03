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
            <picture-outlined />
          </template>
          图片资源生成
        </a-menu-item>
        <a-menu-item key="2">
          <template #icon>
            <video-camera-outlined />
          </template>
          视频资源生成
        </a-menu-item>
        <a-menu-item key="3">
          <template #icon>
            <folder-outlined />
          </template>
          资源库
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout-content style="padding: 24px; min-height: 280px">
      <image-resource-generator
        v-if="selectedKey === '1'"
        @resource-generated="handleResourceGenerated"
      />
      <video-resource-generator
        v-if="selectedKey === '2'"
        @resource-generated="handleResourceGenerated"
      />
      <resource-library v-if="selectedKey === '3'" :resources="generatedResources" />
    </a-layout-content>
  </a-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { PictureOutlined, VideoCameraOutlined, FolderOutlined } from '@ant-design/icons-vue';
import ImageResourceGenerator from './resources/ImageResourceGenerator.vue';
import VideoResourceGenerator from './resources/VideoResourceGenerator.vue';
import ResourceLibrary from './resources/ResourceLibrary.vue';
import { Resource } from '@/types/resources';

const selectedKey = ref('1');
const generatedResources = ref<Resource[]>([]);

const onSelect = (e: { key: string }) => {
  selectedKey.value = e.key;
};

const handleResourceGenerated = (resource: Resource) => {
  // 添加时间戳
  resource.data.createdAt = new Date().toLocaleString();
  generatedResources.value.push(resource);
};
</script>
