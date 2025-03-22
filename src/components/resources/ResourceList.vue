<template>
  <a-spin :spinning="loading">
    <a-list :grid="{ gutter: 16, column: 3 }" :data-source="resources">
      <template #renderItem="{ item }">
        <a-list-item>
          <a-card :title="item.type" size="small" :hoverable="true">
            <template #extra>
              <a-dropdown>
                <template #overlay>
                  <a-menu>
                    <a-menu-item key="download" @click="handleDownload(item)">
                      <download-outlined /> 下载
                    </a-menu-item>
                    <a-menu-item key="preview" @click="handlePreview(item)">
                      <eye-outlined /> 预览
                    </a-menu-item>
                  </a-menu>
                </template>
                <a-button type="link">
                  <more-outlined />
                </a-button>
              </a-dropdown>
            </template>

            <div class="resource-thumbnail">
              <img
                v-if="item.type === '图片'"
                :src="item.data.url"
                :alt="item.data.description || '图片资源'"
              />
              <div v-else-if="item.type === '视频'" class="video-thumbnail">
                <play-circle-outlined />
              </div>
            </div>

            <div class="resource-info">
              <p class="description" v-if="item.data.description">
                {{ truncateText(item.data.description, 50) }}
              </p>
              <p class="timestamp" v-if="item.data.createdAt">创建于: {{ item.data.createdAt }}</p>
            </div>
          </a-card>
        </a-list-item>
      </template>
    </a-list>
  </a-spin>

  <!-- 预览模态框 -->
  <a-modal
    :visible="previewVisible"
    :title="previewResource?.data?.description || '资源预览'"
    @cancel="previewVisible = false"
    :footer="null"
    :width="720"
  >
    <img
      v-if="previewResource?.type === '图片'"
      :src="previewResource?.data?.url"
      alt="预览图片"
      style="max-width: 100%"
    />
    <video
      v-else-if="previewResource?.type === '视频'"
      :src="previewResource?.data?.url"
      controls
      style="width: 100%"
    ></video>
  </a-modal>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { message } from 'ant-design-vue';
import {
  DownloadOutlined,
  EyeOutlined,
  MoreOutlined,
  PlayCircleOutlined,
} from '@ant-design/icons-vue';
import { Resource } from '@/types/resources';

defineProps<{
  resources: Resource[];
}>();

const loading = ref(false);
const previewVisible = ref(false);
const previewResource = ref<Resource | null>(null);

const truncateText = (text: string, maxLength: number) => {
  if (!text) return '';
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
};

const handleDownload = (resource: Resource) => {
  message.success('开始下载资源');
  // 实际实现下载逻辑
  const link = document.createElement('a');
  link.href = resource.data.url;
  link.download = `resource-${Date.now()}.${resource.type === '图片' ? 'jpg' : 'mp4'}`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

const handlePreview = (resource: Resource) => {
  previewResource.value = resource;
  previewVisible.value = true;
};
</script>

<style scoped>
.resource-thumbnail {
  height: 150px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
  margin-bottom: 8px;
  border-radius: 4px;
  overflow: hidden;
}

.resource-thumbnail img {
  max-width: 100%;
  max-height: 100%;
  object-fit: cover;
}

.video-thumbnail {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background-color: #e6f7ff;
  font-size: 48px;
  color: #1890ff;
}

.resource-info {
  margin-top: 8px;
}

.description {
  margin-bottom: 4px;
  font-size: 14px;
}

.timestamp {
  color: #999;
  font-size: 12px;
  margin: 0;
}
</style>
