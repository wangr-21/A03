<!-- eslint-disable @typescript-eslint/no-unused-vars -->
<script setup lang="ts">
import { reactive, ref, watch, computed, capitalize } from 'vue';
import type { UploadUserFile } from 'element-plus';
import { uploadImage } from '@/api';
import type { PostForm } from '@/api';
import { ElMessage } from 'element-plus';

const props = defineProps<{
  visible: boolean;
  isPosting: boolean;
  availableTags: string[];
  initialType?: string;
  initialTags?: string[];
}>();

const emit = defineEmits(['update:visible', 'submit-post']);

// 表单数据
const postForm = reactive<PostForm>({
  title: '',
  content: '',
  type: props.initialType || 'article',
  images: [] as UploadUserFile[],
  attachments: [] as UploadUserFile[],
  tags: props.initialTags || [],
  mentionedUsers: [] as string[],
});

// 编辑器状态
const editorState = reactive({
  isBold: false,
  isItalic: false,
  isList: false,
  showEmojiPicker: false,
  showMentionPanel: false,
  isDraft: false,
});

// 是否显示预览
const showPreview = ref(false);

// 自动保存计时器
const autoSaveTimer = ref<number | null>(null);

// 计算字数
const wordCount = computed(() => {
  return postForm.content.length;
});

// 监听对话框可见性变化
watch(
  () => props.visible,
  (visible) => {
    if (visible) {
      loadDraft();
    } else {
      clearAutoSave();
    }
  },
);

// 监听内容变化，自动保存
watch(
  () => postForm.content,
  () => {
    if (autoSaveTimer.value) {
      clearTimeout(autoSaveTimer.value);
    }
    autoSaveTimer.value = setTimeout(() => {
      saveDraft();
    }, 3000) as unknown as number;
  },
);

// 加载草稿
const loadDraft = () => {
  const draft = localStorage.getItem('post_draft');
  if (draft) {
    const draftData = JSON.parse(draft);
    Object.assign(postForm, draftData);
    editorState.isDraft = true;
    ElMessage.info('已加载上次的草稿');
  } else {
    resetForm();
  }
};

// 保存草稿
const saveDraft = () => {
  localStorage.setItem('post_draft', JSON.stringify(postForm));
  editorState.isDraft = true;
};

// 清除自动保存
const clearAutoSave = () => {
  if (autoSaveTimer.value) {
    clearTimeout(autoSaveTimer.value);
    autoSaveTimer.value = null;
  }
};

// 重置表单
const resetForm = () => {
  postForm.title = '';
  postForm.content = '';
  postForm.type = props.initialType || 'article';
  postForm.images = [];
  postForm.attachments = [];
  postForm.tags = props.initialTags || [];
  postForm.mentionedUsers = [];
  showPreview.value = false;
  editorState.isDraft = false;
  localStorage.removeItem('post_draft');
};

// 切换预览
const togglePreview = () => {
  showPreview.value = !showPreview.value;
};

// 编辑器功能
const toggleFormat = (type: 'bold' | 'italic' | 'list') => {
  const key = `is${capitalize(type)}` as const;
  editorState[key] = !editorState[key];

  const textarea = document.querySelector('.content-editor') as HTMLTextAreaElement;
  if (!textarea) return;

  const start = textarea.selectionStart;
  const end = textarea.selectionEnd;
  const selectedText = postForm.content.substring(start, end);

  let newText = '';
  switch (type) {
    case 'bold':
      newText = `**${selectedText}**`;
      break;
    case 'italic':
      newText = `*${selectedText}*`;
      break;
    case 'list':
      newText = selectedText
        .split('\n')
        .map((line) => `- ${line}`)
        .join('\n');
      break;
  }

  postForm.content =
    postForm.content.substring(0, start) + newText + postForm.content.substring(end);
};

// 插入表情
const insertEmoji = (emoji: string) => {
  const textarea = document.querySelector('.content-editor') as HTMLTextAreaElement;
  if (!textarea) return;

  const start = textarea.selectionStart;
  postForm.content =
    postForm.content.substring(0, start) + emoji + postForm.content.substring(start);

  editorState.showEmojiPicker = false;
};

// 提及用户
const mentionUser = (username: string) => {
  const textarea = document.querySelector('.content-editor') as HTMLTextAreaElement;
  if (!textarea) return;

  const start = textarea.selectionStart;
  postForm.content =
    postForm.content.substring(0, start) + `@${username} ` + postForm.content.substring(start);

  if (!postForm.mentionedUsers.includes(username)) {
    postForm.mentionedUsers.push(username);
  }

  editorState.showMentionPanel = false;
};

// 图片上传处理
const handlePostImageUpload = (uploadFile: UploadUserFile) => {
  if (uploadFile.raw) {
    if (uploadFile.raw.size > 5 * 1024 * 1024) {
      ElMessage.warning('图片大小不能超过5MB');
      return;
    }

    uploadImage(uploadFile.raw as File)
      .then((response) => {
        if (response.success) {
          ElMessage.success('图片上传成功');
        } else {
          ElMessage.error('图片上传失败');
        }
      })
      .catch((error) => {
        ElMessage.error('图片上传出错');
        console.error('Error uploading image:', error);
      });
  }
};

// 附件上传处理
const handlePostAttachmentUpload = (uploadFile: UploadUserFile) => {
  if (uploadFile.raw) {
    const fileSize = (uploadFile.raw as File).size / 1024 / 1024;
    if (fileSize > 50) {
      ElMessage.warning('文件大小不能超过50MB');
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
  if (!postForm.title.trim()) {
    ElMessage.warning('请输入标题');
    return;
  }
  if (!postForm.content.trim()) {
    ElMessage.warning('请输入内容');
    return;
  }

  emit('submit-post', { ...postForm });
  localStorage.removeItem('post_draft');
};

// 关闭对话框
const closeDialog = () => {
  if (editorState.isDraft) {
    ElMessage.info('已自动保存为草稿');
  }
  emit('update:visible', false);
};
</script>

<template>
  <el-dialog
    :model-value="visible"
    @update:model-value="(val: boolean) => emit('update:visible', val)"
    :title="
      postForm.type === 'article'
        ? '发布文章'
        : postForm.type === 'image'
          ? '图片分享'
          : postForm.type === 'resource'
            ? '资源分享'
            : '提问求助'
    "
    width="65%"
    top="5vh"
    destroy-on-close
  >
    <div class="post-type-tabs">
      <el-radio-group v-model="postForm.type" size="large">
        <el-radio-button label="article">
          <el-icon><Edit /></el-icon>文章
        </el-radio-button>
        <el-radio-button label="image">
          <el-icon><Picture /></el-icon>图片
        </el-radio-button>
        <el-radio-button label="resource">
          <el-icon><Paperclip /></el-icon>资源
        </el-radio-button>
        <el-radio-button label="question">
          <el-icon><QuestionFilled /></el-icon>提问
        </el-radio-button>
      </el-radio-group>
    </div>

    <div class="post-content" v-show="!showPreview">
      <el-form :model="postForm" label-position="top">
        <el-form-item
          label="标题"
          required
          :rules="[{ required: true, message: '请输入标题', trigger: 'blur' }]"
        >
          <el-input
            v-model="postForm.title"
            placeholder="请输入标题（2-50字）"
            maxlength="50"
            show-word-limit
          ></el-input>
        </el-form-item>

        <el-form-item label="内容" required>
          <div class="editor-toolbar">
            <el-button-group>
              <el-button text
                ><el-icon><Bold /></el-icon
              ></el-button>
              <el-button text
                ><el-icon><Italic /></el-icon
              ></el-button>
              <el-button text
                ><el-icon><List /></el-icon
              ></el-button>
            </el-button-group>
          </div>
          <el-input
            type="textarea"
            v-model="postForm.content"
            :rows="12"
            :placeholder="
              postForm.type === 'article'
                ? '分享您的教学经验和见解...'
                : postForm.type === 'image'
                  ? '添加图片说明...'
                  : postForm.type === 'resource'
                    ? '描述您要分享的资源...'
                    : '详细描述您的问题，以获得更好的帮助...'
            "
            resize="none"
            maxlength="10000"
            show-word-limit
          ></el-input>
        </el-form-item>

        <el-form-item v-if="postForm.type === 'image'" label="上传图片">
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
              <div class="el-upload__tip">支持 JPG、PNG 格式，单张不超过 5MB，最多9张</div>
            </template>
          </el-upload>
        </el-form-item>

        <el-form-item v-if="postForm.type === 'resource'" label="上传资源">
          <el-upload
            action="/api/upload-file"
            v-model:file-list="postForm.attachments"
            :on-change="handlePostAttachmentUpload"
            multiple
            :limit="5"
          >
            <el-button type="primary" plain icon="Upload">上传资源文件</el-button>
            <template #tip>
              <div class="el-upload__tip">
                支持常见文档格式（PDF、Word、PPT等），单个文件不超过50MB，最多5个文件
              </div>
            </template>
          </el-upload>
        </el-form-item>

        <el-form-item label="添加标签">
          <el-select
            v-model="postForm.tags"
            multiple
            filterable
            allow-create
            default-first-option
            placeholder="选择或创建标签（最多5个）"
            style="width: 100%"
            :max="5"
          >
            <el-option v-for="item in availableTags" :key="item" :label="item" :value="item" />
          </el-select>
          <div class="form-tip">热门标签：教学经验、教学设计、教学反思、教学资源、教学工具</div>
        </el-form-item>
      </el-form>
    </div>

    <div v-show="showPreview" class="preview-content">
      <div class="preview-title">{{ postForm.title || '无标题' }}</div>
      <div class="preview-body">{{ postForm.content || '无内容' }}</div>
      <div v-if="postForm.images.length" class="preview-images">
        <el-image
          v-for="img in postForm.images"
          :key="img.uid"
          :src="img.url"
          :preview-src-list="postForm.images.map((i) => i.url)"
          fit="cover"
        />
      </div>
      <div v-if="postForm.attachments.length" class="preview-attachments">
        <div v-for="file in postForm.attachments" :key="file.uid" class="attachment-item">
          <el-icon><Document /></el-icon>
          <span>{{ file.name }}</span>
        </div>
      </div>
      <div v-if="postForm.tags.length" class="preview-tags">
        <el-tag
          v-for="tag in postForm.tags"
          :key="tag"
          size="small"
          effect="plain"
          class="tag-item"
        >
          {{ tag }}
        </el-tag>
      </div>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <div class="footer-left">
          <el-button text @click="togglePreview">
            {{ showPreview ? '返回编辑' : '预览' }}
          </el-button>
        </div>
        <div class="footer-right">
          <el-button @click="closeDialog">取消</el-button>
          <el-button
            type="primary"
            @click="submitPost"
            :loading="isPosting"
            :disabled="!postForm.title.trim() || !postForm.content.trim()"
          >
            {{ isPosting ? '发布中...' : '发布' }}
          </el-button>
        </div>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>
.post-type-tabs {
  margin-bottom: 24px;
  text-align: center;
}

.post-type-tabs :deep(.el-radio-button__inner) {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 12px 24px;
}

.editor-toolbar {
  margin-bottom: 8px;
  padding: 8px;
  border: 1px solid var(--el-border-color-lighter);
  border-bottom: none;
  border-radius: 4px 4px 0 0;
  background: var(--el-bg-color-page);
}

.form-tip {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  margin-top: 4px;
  line-height: 1.4;
}

.dialog-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Preview Styles */
.preview-content {
  padding: 24px;
  background: var(--el-bg-color-page);
  border-radius: 8px;
}

.preview-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin-bottom: 16px;
}

.preview-body {
  font-size: 16px;
  line-height: 1.8;
  color: var(--el-text-color-regular);
  white-space: pre-wrap;
  margin-bottom: 24px;
}

.preview-images {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.preview-images .el-image {
  width: 100%;
  height: 200px;
  border-radius: 8px;
  overflow: hidden;
}

.preview-attachments {
  margin-bottom: 24px;
}

.attachment-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: var(--el-fill-color-lighter);
  border-radius: 4px;
  margin-bottom: 8px;
}

.preview-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-item {
  cursor: default;
}

/* Dialog Styles */
:deep(.el-dialog) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.el-dialog__header) {
  margin: 0;
  padding: 20px 24px;
  border-bottom: 1px solid var(--el-border-color-lighter);
}

:deep(.el-dialog__body) {
  padding: 24px;
}

:deep(.el-dialog__footer) {
  margin: 0;
  padding: 16px 24px;
  border-top: 1px solid var(--el-border-color-lighter);
}
</style>
