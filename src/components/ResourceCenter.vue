<template>
  <el-container style="height: 100vh">
    <el-aside width="200px">
      <el-menu
        mode="vertical"
        :default-active="selectedKey"
        @select="onSelect"
        style="height: 100%; border-right: 0"
      >
        <el-menu-item index="1">
          <el-icon><Picture /></el-icon>
          <span>图片资源生成</span>
        </el-menu-item>
        <el-menu-item index="2">
          <el-icon><VideoCamera /></el-icon>
          <span>视频资源生成</span>
        </el-menu-item>
        <el-menu-item index="3">
          <el-icon><Folder /></el-icon>
          <span>资源库</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-main style="padding: 24px; min-height: 280px">
      <image-resource-generator
        v-if="selectedKey === '1'"
        @resource-generated="handleResourceGenerated"
      />
      <video-resource-generator
        v-if="selectedKey === '2'"
        @resource-generated="handleResourceGenerated"
      />
      <resource-library v-if="selectedKey === '3'" :resources="generatedResources" />
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Picture, VideoCamera, Folder } from '@element-plus/icons-vue';
import ImageResourceGenerator from './resources/ImageResourceGenerator.vue';
import VideoResourceGenerator from './resources/VideoResourceGenerator.vue';
import ResourceLibrary from './resources/ResourceLibrary.vue';
import { Resource } from '@/types/resources';

const selectedKey = ref('1');
const generatedResources = ref<Resource[]>([]);

const onSelect = (key: string) => {
  selectedKey.value = key;
};

const handleResourceGenerated = (resource: Resource) => {
  // 添加时间戳
  resource.data.createdAt = new Date().toLocaleString();
  generatedResources.value.push(resource);
};
</script>
