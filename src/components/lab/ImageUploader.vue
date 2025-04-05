<script setup lang="ts">
import { ElMessage } from 'element-plus';
import type { UploadFile, UploadUserFile } from 'element-plus';

defineProps<{
  title?: string;
  tip?: string;
}>();

const emit = defineEmits<{
  'upload-success': [url: string, file: UploadUserFile];
  'upload-error': [error: Error];
}>();

const onChange = async (file: UploadFile): Promise<void> => {
  try {
    emit('upload-success', URL.createObjectURL(file.raw!), file);
  } catch (error) {
    console.error('Image Upload Error:', error);
    ElMessage.error('图片上传失败!');
    emit('upload-error', error as Error);
  }
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
      action="#"
      :auto-upload="false"
      :show-file-list="false"
      :limit="1"
      :before-upload="beforeUpload"
      :on-change="onChange"
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
