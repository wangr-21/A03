<script setup lang="ts">
import { reactive, watch } from 'vue';
import type { UploadUserFile } from 'element-plus';
import { uploadImage } from '@/api';
import type { PostForm } from '@/api';

const props = defineProps<{
  visible: boolean;
  isPosting: boolean;
  availableTags: string[];
}>();

const emit = defineEmits(['update:visible', 'submit-post']);

// 表单数据
const postForm = reactive<PostForm>({
  content: '',
  images: [] as UploadUserFile[],
  attachments: [] as UploadUserFile[],
  tags: [],
});

// 监听对话框可见性变化，重置表单
watch(
  () => props.visible,
  (visible) => {
    if (visible) {
      resetForm();
    }
  },
);

// 重置表单
const resetForm = () => {
  postForm.content = '';
  postForm.images = [];
  postForm.attachments = [];
  postForm.tags = [];
};

// 图片上传处理
const handlePostImageUpload = (uploadFile: UploadUserFile) => {
  console.log('Image file changed:', uploadFile);

  if (uploadFile.raw) {
    uploadImage(uploadFile.raw as File)
      .then((response) => {
        if (response.success) {
          console.log('Image uploaded successfully:', response.url);
        } else {
          console.error('Failed to upload image');
        }
      })
      .catch((error) => {
        console.error('Error uploading image:', error);
      });
  }
};

// 附件上传处理
const handlePostAttachmentUpload = (uploadFile: UploadUserFile) => {
  console.log('Attachment file changed:', uploadFile);

  if (uploadFile.raw) {
    const fileSize = (uploadFile.raw as File).size / 1024 / 1024; // 转换为MB
    if (fileSize > 50) {
      const index = postForm.attachments.findIndex((file) => file.uid === uploadFile.uid);
      if (index !== -1) {
        postForm.attachments.splice(index, 1);
      }
      return;
    }
  }
};

// 提交帖子
const submitPost = () => {
  if (!postForm.content.trim()) {
    return;
  }
  emit('submit-post', { ...postForm });
};

// 关闭对话框
const closeDialog = () => {
  emit('update:visible', false);
};
</script>

<template>
  <el-dialog
    :model-value="visible"
    @update:model-value="(val: boolean) => emit('update:visible', val)"
    title="发布新帖子"
    width="60%"
    top="8vh"
    destroy-on-close
  >
    <el-form :model="postForm" label-position="top">
      <el-form-item label="分享内容">
        <el-input
          type="textarea"
          v-model="postForm.content"
          :rows="5"
          placeholder="尽情分享您的想法、经验或资源..."
          resize="none"
          maxlength="2000"
          show-word-limit
        ></el-input>
      </el-form-item>
      <el-form-item label="添加图片 (可选)">
        <el-upload
          action="/api/upload-image"
          list-type="picture-card"
          v-model:file-list="postForm.images"
          :on-change="handlePostImageUpload"
          multiple
          accept="image/*"
          :limit="9"
        >
          <el-icon><Plus /></el-icon>
          <template #tip>
            <div class="el-upload__tip">支持 JPG、PNG 格式，单张不超过 5MB</div>
          </template>
        </el-upload>
      </el-form-item>
      <el-form-item label="添加附件 (可选)">
        <el-upload
          action="/api/upload-file"
          v-model:file-list="postForm.attachments"
          :on-change="handlePostAttachmentUpload"
          multiple
          :limit="5"
        >
          <el-button type="primary" plain icon="Upload">点击上传附件</el-button>
          <template #tip>
            <div class="el-upload__tip">文件大小不超过 50MB，支持各种常见文档格式</div>
          </template>
        </el-upload>
      </el-form-item>
      <el-form-item label="添加话题标签 (可选)">
        <el-select
          v-model="postForm.tags"
          multiple
          filterable
          allow-create
          default-first-option
          placeholder="选择或创建话题标签"
          style="width: 100%"
          :max="5"
        >
          <el-option v-for="item in availableTags" :key="item" :label="item" :value="item" />
        </el-select>
        <div class="form-tip">最多添加5个标签，每个标签不超过10个字符</div>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="closeDialog">取消</el-button>
        <el-button
          type="primary"
          @click="submitPost"
          :loading="isPosting"
          :disabled="!postForm.content.trim()"
        >
          {{ isPosting ? '发布中...' : '确认发布' }}
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<style scoped>
.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
  line-height: 1.4;
}

/* Dialog Styles */
:deep(.el-dialog__body) .el-form-item {
  margin-bottom: 20px;
}

:deep(.el-dialog) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.el-dialog__header) {
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
}

:deep(.el-dialog__body) {
  padding: 20px 30px;
}

:deep(.el-dialog__footer) {
  padding: 15px 20px 20px;
  border-top: 1px solid #f0f0f0;
}

:deep(.el-upload-list--picture-card) .el-upload--picture-card {
  width: 100px;
  height: 100px;
  border-radius: 8px;
  line-height: 100px;
  transition: all 0.3s ease;
}

:deep(.el-upload-list--picture-card) .el-upload--picture-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

:deep(.el-upload-list--picture-card) .el-upload-list__item {
  width: 100px;
  height: 100px;
  border-radius: 8px;
  margin: 0 8px 8px 0;
}
</style>
