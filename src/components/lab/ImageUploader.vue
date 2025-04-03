<script setup lang="ts">
import { ElMessage } from 'element-plus';
import type { UploadUserFile } from 'element-plus';
import { uploadImage } from '@/api';

defineProps<{
  title?: string;
  tip?: string;
}>();

const emit = defineEmits(['upload-success', 'upload-error']);

const handleUploadSuccess = async (
  response: unknown,
  uploadFile: UploadUserFile,
): Promise<void> => {
  try {
    const result = await uploadImage(uploadFile.raw as File);
    if (result.success) {
      emit('upload-success', {
        url: result.url || URL.createObjectURL(uploadFile.raw!),
        file: uploadFile,
      });
    } else {
      throw new Error(result.message || 'Upload failed');
    }
  } catch (error) {
    console.error('Image Upload Error:', error);
    ElMessage.error('图片上传失败!');
    emit('upload-error', error);
  }
};

const handleUploadError = (
  error: Error,
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  uploadFile: UploadUserFile,
): void => {
  ElMessage.error('图片上传失败!');
  console.error('Upload Error:', error);
  emit('upload-error', error);
};

const beforeUpload = (rawFile: File): boolean | Promise<File> => {
  if (!rawFile.type.startsWith('image/')) {
    ElMessage.error('只能上传图片文件!');
    return false;
  }
  if (rawFile.size / 1024 / 1024 > 5) {
    // Limit size to 5MB
    ElMessage.error('图片大小不能超过 5MB!');
    return false;
  }
  return true;
};
</script>

<template>
  <div>
    <h4 v-if="title">{{ title }}</h4>
    <el-upload
      class="image-uploader"
      action="/api/upload"
      :show-file-list="false"
      :on-success="handleUploadSuccess"
      :on-error="handleUploadError"
      :before-upload="beforeUpload"
      drag
    >
      <el-icon class="el-icon--upload"><upload-filled /></el-icon>
      <div class="el-upload__text">
        拖拽文件到此处 或 <em>点击上传</em>
        <div class="upload-tip" v-if="tip">{{ tip }}</div>
        <div class="upload-tip" v-else>(JPG/PNG, &lt;5MB)</div>
      </div>
    </el-upload>
  </div>
</template>

<style scoped>
.image-uploader {
  margin-bottom: 15px;
  border: 2px dashed var(--el-border-color);
  border-radius: 6px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.3s ease;
}
.image-uploader:hover {
  border-color: var(--el-color-primary);
}
.upload-tip {
  font-size: 12px;
  color: #666;
  margin-top: 5px;
}
</style>
