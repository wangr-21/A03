<template>
  <a-card title="图片资源生成">
    <template #extra>
      <picture-outlined style="font-size: 24px" />
    </template>
    <a-form
      layout="vertical"
      @finish="handleGenerateImage"
      :model="formState"
      ref="formRef"
      :validate-trigger="['submit']"
    >
      <a-form-item
        name="imageType"
        label="图片类型"
        :rules="[{ required: true, message: '请选择图片类型' }]"
      >
        <a-select v-model:value="formState.imageType" placeholder="请选择图片类型" allow-clear>
          <a-select-option value="concept">教学概念可视化</a-select-option>
          <a-select-option value="mindmap">思维导图</a-select-option>
          <a-select-option value="scene">教学情境插图</a-select-option>
        </a-select>
      </a-form-item>
      <a-form-item
        name="description"
        label="图片描述"
        :rules="[{ required: true, message: '请描述您需要的图片内容' }]"
      >
        <a-textarea
          v-model:value="formState.description"
          :rows="4"
          placeholder="请描述您需要的图片内容"
        ></a-textarea>
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit">生成图片</a-button>
      </a-form-item>
    </a-form>

    <div class="preview-container" v-if="previewImage">
      <h3>图片预览</h3>
      <img :src="previewImage" alt="生成的图片" class="preview-image" />
      <a-button type="primary" @click="saveGeneratedResource" style="margin-top: 16px">
        保存到资源库
      </a-button>
    </div>
  </a-card>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { message } from 'ant-design-vue';
import { PictureOutlined } from '@ant-design/icons-vue';
import type { FormInstance } from 'ant-design-vue';
import type { Resource } from '@/types/resources';

const emit = defineEmits(['resource-generated']);
const previewImage = ref('');
const formRef = ref<FormInstance>();

const handleResourceGenerated = (resource: Resource) => {
  resource.data.createdAt = new Date().toLocaleString();
  emit('resource-generated', resource);
};

// 表单状态 - 使用 undefined 而不是空字符串
const formState = reactive({
  imageType: undefined as string | undefined,
  description: '',
});

let currentImageData: {
  url: string;
  type: string;
  description: string;
} | null = null;

interface ImageFormData {
  imageType: 'concept' | 'mindmap' | 'scene';
  description: string;
}

const handleGenerateImage = async (values: ImageFormData) => {
  try {
    message.loading({ content: '正在生成图片资源...', key: 'imageResource' });

    // 这里应该使用实际的API调用
    // const response = await api.generateImageResource(values);

    // 模拟API响应
    setTimeout(() => {
      const imageTypeLabels = {
        concept: '教学概念可视化',
        mindmap: '思维导图',
        scene: '教学情境插图',
      };

      message.success({ content: '图片资源生成成功！', key: 'imageResource' });

      // 使用placeholder.pics生成一个模拟图片
      const placeholderUrl = `https://placeholder.pics/svg/400x300/DEDEDE/555555/${encodeURIComponent(
        values.imageType
      )}`;
      previewImage.value = placeholderUrl;

      // 保存当前图片数据以供后续使用
      currentImageData = {
        url: placeholderUrl,
        type: imageTypeLabels[values.imageType],
        description: values.description,
      };
    }, 1500);
  } catch (error) {
    message.error({
      content: '生成图片资源失败，请重试',
      key: 'imageResource',
    });
    console.error('生成图片资源错误:', error);
  }
};

const saveGeneratedResource = () => {
  if (currentImageData) {
    handleResourceGenerated({
      type: '图片',
      data: currentImageData,
    });
    message.success('图片已成功保存到资源库');

    // 重置预览和表单
    previewImage.value = '';
    currentImageData = null;
    formRef.value?.resetFields();
  }
};
</script>

<style scoped>
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
