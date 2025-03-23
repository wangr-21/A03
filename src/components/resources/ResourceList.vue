<template>
  <el-container v-loading="loading">
    <el-row :gutter="16" style="width: 100%">
      <el-col
        :xs="24"
        :sm="12"
        :md="8"
        v-for="(item, index) in resources"
        :key="index"
        style="margin-bottom: 16px"
      >
        <el-card :body-style="{ padding: '0px' }" shadow="hover">
          <div style="position: relative">
            <div class="resource-thumbnail">
              <img
                v-if="item.type === '图片'"
                :src="item.data.url"
                :alt="item.data.description || '图片资源'"
              />
              <div v-else-if="item.type === '视频'" class="video-thumbnail">
                <el-icon><VideoPlay /></el-icon>
              </div>
            </div>

            <div class="resource-actions">
              <el-dropdown trigger="click">
                <el-button type="primary" size="small" circle>
                  <el-icon><More /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item @click="handleDownload(item)">
                      <el-icon><Download /></el-icon> 下载
                    </el-dropdown-item>
                    <el-dropdown-item @click="handlePreview(item)">
                      <el-icon><View /></el-icon> 预览
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>

          <div style="padding: 14px">
            <div class="resource-title">{{ item.type }}</div>
            <div class="resource-info">
              <p class="description" v-if="item.data.description">
                {{ truncateText(item.data.description, 50) }}
              </p>
              <p class="timestamp" v-if="item.data.createdAt">创建于: {{ item.data.createdAt }}</p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 预览对话框 -->
    <el-dialog
      v-model="previewVisible"
      :title="previewResource?.data?.description || '资源预览'"
      width="70%"
      destroy-on-close
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
    </el-dialog>
  </el-container>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import { Download, View, VideoPlay, More } from '@element-plus/icons-vue';
import type { Resource } from '@/types/resources';

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
  ElMessage.success('开始下载资源');
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
  overflow: hidden;
}

.resource-thumbnail img {
  width: 100%;
  height: 100%;
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
  color: #409eff;
}

.resource-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 8px;
  color: #303133;
}

.resource-info {
  margin-top: 8px;
}

.description {
  margin-bottom: 4px;
  font-size: 14px;
  color: #606266;
}

.timestamp {
  color: #909399;
  font-size: 12px;
  margin: 0;
}

.resource-actions {
  position: absolute;
  top: 8px;
  right: 8px;
  z-index: 10;
}
</style>
