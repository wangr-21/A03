<script setup lang="ts">
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import type { UploadUserFile } from 'element-plus';
import { getAvailableStyles, applyStyleTransfer } from '@/api';
import type { StyleOption } from '@/api';
import ImageUploader from './ImageUploader.vue';

// --- State for Style Transfer ---
const styleTransferFile = ref<UploadUserFile | null>(null);
const styleTransferImageUrl = ref<string>('');
const styleTransferResultUrl = ref<string>('');
const availableStyles = ref<StyleOption[]>(getAvailableStyles()); // 直接使用API提供的样式列表
const selectedStyle = ref<string>(availableStyles.value[0]?.key || '');
const isApplyingStyle = ref<boolean>(false);

// Upload handler
const handleStyleUploadSuccess = (url: string, file: UploadUserFile) => {
  styleTransferImageUrl.value = url;
  styleTransferFile.value = file;
  styleTransferResultUrl.value = ''; // Clear previous result
};

// Apply style transfer
const applyStyleTransferFunc = async (): Promise<void> => {
  if (!styleTransferFile.value || !selectedStyle.value) {
    ElMessage.warning('请先上传图片并选择风格！');
    return;
  }
  isApplyingStyle.value = true;
  console.log('Applying style:', selectedStyle.value, 'to file:', styleTransferFile.value.name);

  try {
    const result = await applyStyleTransfer(styleTransferFile.value, selectedStyle.value);
    styleTransferResultUrl.value = result.resultUrl;
    ElMessage.success('风格转换成功！');
  } catch (error) {
    console.error('Error applying style transfer:', error);
    ElMessage.error('风格转换失败，请稍后重试');
  } finally {
    isApplyingStyle.value = false;
  }
};

// Download style transfer result
const downloadResult = () => {
  if (!styleTransferResultUrl.value) return;

  const link = document.createElement('a');
  link.href = styleTransferResultUrl.value;
  link.download = `style_transfer_${Date.now()}.jpg`;
  link.click();
};
</script>

<template>
  <el-card class="tool-panel">
    <el-row :gutter="30">
      <!-- Left: Upload & Original Image -->
      <el-col :span="10">
        <ImageUploader
          title="1. 上传原始图片"
          @upload-success="handleStyleUploadSuccess"
        />
        <div class="image-preview" v-if="styleTransferImageUrl">
          <h5>原图预览</h5>
          <el-image :src="styleTransferImageUrl" fit="contain"></el-image>
        </div>
      </el-col>

      <!-- Middle: Style Selection -->
      <el-col :span="4">
        <h4>2. 选择艺术风格</h4>
        <div class="style-selector">
          <div
            v-for="style in availableStyles"
            :key="style.key"
            class="style-option"
            :class="{ 'is-active': selectedStyle === style.key }"
            @click="selectedStyle = style.key"
          >
            <el-image :src="style.thumb" fit="cover"></el-image>
            <span>{{ style.name }}</span>
          </div>
        </div>
      </el-col>

      <!-- Right: Result & Action -->
      <el-col :span="10">
        <h4>3. 生成风格化图片</h4>
        <div
          class="result-area"
          v-loading="isApplyingStyle"
          element-loading-text="正在应用风格..."
        >
          <div class="image-preview result-preview" v-if="styleTransferResultUrl">
            <h5>效果预览</h5>
            <el-image :src="styleTransferResultUrl" fit="contain"></el-image>
            <div class="result-actions">
              <el-button type="primary" icon="Download" @click="downloadResult">下载图片</el-button>
            </div>
          </div>
          <el-empty v-else description="请上传图片并选择风格后点击生成"></el-empty>
        </div>
        <el-button
          type="primary"
          @click="applyStyleTransferFunc"
          :disabled="!styleTransferImageUrl || !selectedStyle || isApplyingStyle"
          :loading="isApplyingStyle"
          class="action-button"
          icon="MagicStick"
        >
          {{ isApplyingStyle ? '正在转换...' : '开始风格转换' }}
        </el-button>
      </el-col>
    </el-row>
  </el-card>
</template>

<style scoped>
.tool-panel {
  padding: 20px;
}

.tool-panel h4 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 15px;
  color: #333;
}

.image-preview {
  margin-top: 15px;
  border: 1px solid #eee;
  padding: 10px;
  border-radius: 4px;
  min-height: 150px; /* Ensure some height even before image loads */
  display: flex;
  flex-direction: column;
  align-items: center;
}
.image-preview h5 {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}
.image-preview .el-image {
  max-width: 100%;
  max-height: 300px; /* Limit preview height */
}

.action-button {
  margin-top: 20px;
  width: 100%;
}

/* Style Transfer Specific */
.style-selector {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: 400px; /* Allow scrolling for many styles */
  overflow-y: auto;
}
.style-option {
  border: 2px solid transparent;
  padding: 5px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}
.style-option.is-active {
  border-color: var(--el-color-primary);
  background-color: var(--el-color-primary-light-9);
}
.style-option:hover {
  background-color: #f5f7fa;
}
.style-option .el-image {
  width: 80px;
  height: 80px;
  border-radius: 4px;
  margin-bottom: 5px;
}
.style-option span {
  font-size: 13px;
  color: #333;
}

.result-area {
  border: 1px dashed #dcdfe6;
  border-radius: 6px;
  min-height: 300px; /* Match image preview height */
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 15px;
}
.result-preview {
  border: none;
  padding: 0;
  margin-top: 0;
}
.result-actions {
  margin-top: 15px;
  text-align: center;
}
</style>
