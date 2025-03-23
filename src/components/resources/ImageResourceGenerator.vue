<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>图片资源生成</span>
        <el-icon :size="24"><Picture /></el-icon>
      </div>
    </template>

    <el-form
      :model="formState"
      ref="formRef"
      label-position="top"
      @submit.prevent="handleGenerateImage"
    >
      <el-form-item
        label="图片类型"
        prop="imageType"
        :rules="[{ required: true, message: '请选择图片类型', trigger: 'change' }]"
      >
        <el-select
          v-model="formState.imageType"
          placeholder="请选择图片类型"
          clearable
          style="width: 100%"
        >
          <el-option label="教学概念可视化" value="concept" />
          <el-option label="思维导图" value="mindmap" />
          <el-option label="教学情境插图" value="scene" />
        </el-select>
      </el-form-item>

      <el-form-item
        label="图片描述"
        prop="description"
        :rules="[{ required: true, message: '请描述您需要的图片内容', trigger: 'blur' }]"
      >
        <el-input
          v-model="formState.description"
          type="textarea"
          :rows="4"
          placeholder="请描述您需要的图片内容"
        ></el-input>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" native-type="submit">生成图片</el-button>
      </el-form-item>
    </el-form>

    <div class="preview-container" v-if="previewImage">
      <h3>图片预览</h3>
      <img :src="previewImage" alt="生成的图片" class="preview-image" />
      <el-button type="primary" @click="saveGeneratedResource" style="margin-top: 16px">
        保存到资源库
      </el-button>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { ElMessage } from 'element-plus';
import { Picture } from '@element-plus/icons-vue';
import type { FormInstance } from 'element-plus';
import type { Resource } from '@/types/resources';

const emit = defineEmits(['resource-generated']);
const previewImage = ref('');
const formRef = ref<FormInstance>();

const handleResourceGenerated = (resource: Resource) => {
  resource.data.createdAt = new Date().toLocaleString();
  emit('resource-generated', resource);
};

// 表单状态
const formState = reactive({
  imageType: '',
  description: '',
});

let currentImageData: {
  url: string;
  type: string;
  description: string;
} | null = null;

// interface ImageFormData {
//   imageType: 'concept' | 'mindmap' | 'scene';
//   description: string;
// }

const handleGenerateImage = async () => {
  await formRef.value?.validate((valid) => {
    if (!valid) return;
    generateImage();
  });
};

const generateImage = async () => {
  try {
    ElMessage({
      message: '正在生成图片资源...',
      type: 'info',
      duration: 0,
      showClose: true,
      grouping: true,
      // id: 'imageResource',
    });

    // 这里应该使用实际的API调用
    // const response = await api.generateImageResource(formState);

    // 模拟API响应
    setTimeout(() => {
      const imageTypeLabels: Record<string, string> = {
        concept: '教学概念可视化',
        mindmap: '思维导图',
        scene: '教学情境插图',
      };

      ElMessage.closeAll();
      ElMessage.success('图片资源生成成功！');

      // 使用placeholder.pics生成一个模拟图片
      const placeholderUrl = `https://placeholder.pics/svg/400x300/DEDEDE/555555/${encodeURIComponent(
        formState.imageType
      )}`;
      previewImage.value = placeholderUrl;

      // 保存当前图片数据以供后续使用
      currentImageData = {
        url: placeholderUrl,
        type: imageTypeLabels[formState.imageType] || formState.imageType,
        description: formState.description,
      };
    }, 1500);
  } catch (error) {
    ElMessage.error('生成图片资源失败，请重试');
    console.error('生成图片资源错误:', error);
  }
};

const saveGeneratedResource = () => {
  if (currentImageData) {
    handleResourceGenerated({
      type: '图片',
      data: currentImageData,
    });
    ElMessage.success('图片已成功保存到资源库');

    // 重置预览和表单
    previewImage.value = '';
    currentImageData = null;
    formRef.value?.resetFields();
  }
};
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.preview-container {
  margin-top: 24px;
  text-align: center;
}

.preview-image {
  max-width: 100%;
  max-height: 400px;
  border: 1px solid #eee;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>
