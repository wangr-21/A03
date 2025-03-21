<template>
  <a-card title="艺术风格转化器" class="style-converter-card">
    <a-form
      layout="vertical"
      @finish="handleStyleConversion"
      :model="formState"
      ref="formRef"
      :validate-trigger="['submit']"
    >
      <a-form-item name="originalImage" label="上传原始图片">
        <a-upload
          v-model:fileList="fileList"
          list-type="picture-card"
          :before-upload="beforeUpload"
          :maxCount="1"
          @preview="handlePreview"
          @change="handleFileChange"
        >
          <div v-if="fileList.length < 1">
            <plus-outlined />
            <div style="margin-top: 8px">上传</div>
          </div>
        </a-upload>
        <a-modal
          :visible="previewVisible"
          :title="previewTitle"
          :footer="null"
          @cancel="handleCancelPreview"
        >
          <img alt="预览图片" style="width: 100%" :src="previewImage" />
        </a-modal>
      </a-form-item>

      <a-form-item
        name="styleType"
        label="选择艺术风格"
        :rules="[{ required: true, message: '请选择艺术风格' }]"
      >
        <a-select
          v-model:value="formState.styleType"
          placeholder="请选择要转换的艺术风格"
          allow-clear
        >
          <a-select-option value="impressionist">印象派</a-select-option>
          <a-select-option value="cubism">立体主义</a-select-option>
          <a-select-option value="ink">中国水墨画</a-select-option>
          <a-select-option value="vangogh">梵高风格</a-select-option>
          <a-select-option value="pop">波普艺术</a-select-option>
        </a-select>
      </a-form-item>

      <a-form-item>
        <a-button
          type="primary"
          html-type="submit"
          :loading="converting"
          :disabled="fileList.length === 0"
        >
          转换风格
        </a-button>
        <a-button style="margin-left: 8px" @click="resetForm" v-if="resultImage">
          重新转换
        </a-button>
      </a-form-item>
    </a-form>

    <a-divider v-if="resultImage" />

    <div v-if="resultImage" class="result-container">
      <h3>转换结果</h3>
      <div class="image-comparison">
        <div class="image-card">
          <p>原图</p>
          <img :src="originalImageUrl" alt="原始图片" class="preview-image" />
        </div>
        <div class="image-card">
          <p>{{ getStyleName(formState.styleType) }}风格</p>
          <img :src="resultImage" alt="转换后图片" class="preview-image" />
          <a-button type="primary" @click="downloadImage" style="margin-top: 16px">
            <download-outlined /> 下载图片
          </a-button>
        </div>
      </div>
    </div>
  </a-card>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { message } from 'ant-design-vue';
import { PlusOutlined, DownloadOutlined } from '@ant-design/icons-vue';
import type { UploadProps } from 'ant-design-vue';
import type { FormInstance } from 'ant-design-vue';

// 表单引用
const formRef = ref<FormInstance>();

// 表单状态
const formState = reactive({
  styleType: undefined as string | undefined,
});

// 文件上传相关
const fileList = ref<any[]>([]);
const previewVisible = ref(false);
const previewImage = ref('');
const previewTitle = ref('');

// 转换状态和结果
const converting = ref(false);
const resultImage = ref('');
const originalImageUrl = ref('');

// 处理文件变化
const handleFileChange = () => {
  formRef.value?.validateFields(['originalImage']);
};

// 上传图片前的验证
const beforeUpload: UploadProps['beforeUpload'] = (file) => {
  const validTypes = ['image/png', 'image/jpeg'];

  if (!validTypes.includes(file.type)) {
    message.error('您只能上传JPG或PNG格式的图片!');
    return false;
  }

  if (file.size / 1024 / 1024 > 2) {
    message.error('图片必须小于2MB!');
    return false;
  }

  // 创建原图的URL
  originalImageUrl.value = URL.createObjectURL(file);
  return false; // 阻止自动上传
};

// 预览图片
const handlePreview = async (file: any) => {
  if (!file.url && !file.preview) {
    file.preview = await getBase64(file.originFileObj);
  }
  previewImage.value = file.url || file.preview;
  previewVisible.value = true;
  previewTitle.value = file.name || file.url.substring(file.url.lastIndexOf('/') + 1);
};

// 取消预览
const handleCancelPreview = () => {
  previewVisible.value = false;
};

// 获取Base64编码的图片
const getBase64 = (file: Blob): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = (error) => reject(error);
  });
};

// 获取风格名称
const getStyleName = (styleType: string | undefined): string => {
  if (!styleType) return '';
  const styleMap: Record<string, string> = {
    impressionist: '印象派',
    cubism: '立体主义',
    ink: '中国水墨画',
    vangogh: '梵高',
    pop: '波普艺术',
  };
  return styleMap[styleType] || styleType;
};

// 处理风格转换
const handleStyleConversion = async () => {
  if (fileList.value.length === 0) {
    message.error('请先上传图片');
    return;
  }
  if (!formState.styleType) {
    message.error('请选择艺术风格');
    return;
  }

  try {
    converting.value = true;
    message.loading({ content: '正在转换风格，请稍候...', key: 'styleConversion' });

    // 获取文件对象
    const file = fileList.value[0].originFileObj;

    // 创建FormData对象
    const formData = new FormData();
    formData.append('image', file);
    formData.append('style', formState.styleType);

    // 模拟API调用
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // 模拟响应结果（使用原图模拟）
    resultImage.value = originalImageUrl.value;

    message.success({ content: '风格转换成功!', key: 'styleConversion' });
  } catch (error) {
    console.error('风格转换失败:', error);
    message.error({ content: '风格转换失败，请重试', key: 'styleConversion' });
  } finally {
    converting.value = false;
  }
};

// 下载转换后的图片
const downloadImage = () => {
  if (!resultImage.value) return;

  const link = document.createElement('a');
  link.href = resultImage.value;
  link.download = `styled-artwork-${formState.styleType}-${Date.now()}.jpg`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);

  message.success('图片下载开始');
};

// 重置表单的方法
const resetForm = () => {
  formRef.value?.resetFields();
  fileList.value = [];
  resultImage.value = '';
  originalImageUrl.value = '';
};
</script>

<style scoped>
.style-converter-card {
  height: 100%;
  overflow-y: auto;
}

.result-container {
  margin-top: 16px;
  margin-bottom: 24px;
}

.image-comparison {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: center;
  margin-top: 16px;
}

.image-card {
  text-align: center;
  padding: 12px;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  background-color: #fafafa;
  width: 250px;
}

.preview-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 4px;
}
</style>
