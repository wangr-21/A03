<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>资源库</span>
        <el-icon :size="24"><Folder /></el-icon>
      </div>
    </template>

    <el-empty v-if="resources.length === 0" description="暂无资源，请先生成并保存资源" />

    <div v-else>
      <el-tabs v-model="activeTab">
        <el-tab-pane label="全部资源" name="1">
          <resource-list :resources="resources" />
        </el-tab-pane>
        <el-tab-pane label="图片资源" name="2">
          <resource-list :resources="imageResources" />
        </el-tab-pane>
        <el-tab-pane label="视频资源" name="3">
          <resource-list :resources="videoResources" />
        </el-tab-pane>
      </el-tabs>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { Folder } from '@element-plus/icons-vue';
import ResourceList from './ResourceList.vue';
import type { Resource } from '@/types/resources';

const props = defineProps<{
  resources: Resource[];
}>();

const activeTab = ref('1');

const imageResources = computed(() => {
  return props.resources.filter((resource) => resource.type === '图片');
});

const videoResources = computed(() => {
  return props.resources.filter((resource) => resource.type === '视频');
});
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
