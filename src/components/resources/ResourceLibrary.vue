<template>
  <a-card title="资源库">
    <template #extra>
      <folder-outlined style="font-size: 24px" />
    </template>

    <a-empty v-if="resources.length === 0" description="暂无资源，请先生成并保存资源" />

    <div v-else>
      <a-tabs default-active-key="1">
        <a-tab-pane key="1" tab="全部资源">
          <resource-list :resources="resources" />
        </a-tab-pane>
        <a-tab-pane key="2" tab="图片资源">
          <resource-list :resources="imageResources" />
        </a-tab-pane>
        <a-tab-pane key="3" tab="视频资源">
          <resource-list :resources="videoResources" />
        </a-tab-pane>
      </a-tabs>
    </div>
  </a-card>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { FolderOutlined } from '@ant-design/icons-vue';
import ResourceList from './ResourceList.vue';
import type { Resource } from '@/types/resources';

const props = defineProps<{
  resources: Resource[];
}>();

const imageResources = computed(() => {
  return props.resources.filter((resource) => resource.type === '图片');
});

const videoResources = computed(() => {
  return props.resources.filter((resource) => resource.type === '视频');
});
</script>
