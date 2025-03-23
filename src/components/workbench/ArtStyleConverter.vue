<template>
  <el-card header="艺术风格转化器" class="style-converter-card">
    <el-form
      :model="formState"
      ref="formRef"
      label-position="top"
      @submit.prevent="handleStyleConversion"
    >
      <el-form-item label="上传原始图片">
        <el-upload
          v-model:file-list="fileList"
          list-type="picture-card"
          :auto-upload="false"
          :limit="1"
          :on-preview="handlePreview"
          :on-change="handleFileChange"
          :before-upload="beforeUpload"
        >
          <el-icon v-if="fileList.length < 1"><Plus /></el-icon>
          <template #tip>
            <div class="upload-tip">支持jpg、png格式，小于2MB</div>
          </template>
        </el-upload>

        <el-dialog v-model="previewVisible" :title="previewTitle">
          <img :src="previewImage" alt="预览图片" style="width: 100%" />
        </el-dialog>
      </el-form-item>

      <el-form-item
        label="选择艺术风格"
        prop="styleType"
        :rules="[{ required: true, message: '请选择艺术风格', trigger: 'change' }]"
      >
        <el-select
          v-model="formState.styleType"
          placeholder="请选择要转换的艺术风格"
          style="width: 100%"
        >
          <el-option label="印象派" value="impressionist" />
          <el-option label="立体主义" value="cubism" />
          <el-option label="中国水墨画" value="ink" />
          <el-option label="梵高风格" value="vangogh" />
          <el-option label="波普艺术" value="pop" />
        </el-select>
      </el-form-item>

      <el-form-item>
        <el-button
          type="primary"
          native-type="submit"
          :loading="converting"
          :disabled="fileList.length === 0"
        >
          转换风格
        </el-button>
        <el-button @click="resetForm" v-if="resultImage" style="margin-left: 8px">
          重新转换
        </el-button>
      </el-form-item>
    </el-form>

    <el-divider v-if="resultImage" />

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
          <el-button type="primary" @click="downloadImage" style="margin-top: 16px">
            <el-icon><Download /></el-icon> 下载图片
          </el-button>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { ElMessage } from 'element-plus';
import { Plus, Download } from '@element-plus/icons-vue';
import type { UploadFile, UploadProps, FormInstance } from 'element-plus';

const styleMap = {
  impressionist: '印象派',
  cubism: '立体主义',
  ink: '中国水墨画',
  vangogh: '梵高',
  pop: '波普艺术',
};
type StyleType = keyof typeof styleMap;

// 表单引用
const formRef = ref<FormInstance>();

// 表单状态
const formState = reactive({
  styleType: undefined as StyleType | undefined,
});

// 文件上传相关
const fileList = ref<UploadFile[]>([]);
const previewVisible = ref(false);
const previewImage = ref(undefined as string | undefined);
const previewTitle = ref(undefined as string | undefined);

// 转换状态和结果
const converting = ref(false);
const resultImage = ref(undefined as string | undefined);
const originalImageUrl = ref(undefined as string | undefined);

// 处理文件变化
const handleFileChange = () => {
  formRef.value?.validateField('originalImage');
};

// 上传图片前的验证
const beforeUpload: UploadProps['beforeUpload'] = (file) => {
  const validTypes = ['image/png', 'image/jpeg'];

  if (!validTypes.includes(file.type)) {
    ElMessage.error('您只能上传JPG或PNG格式的图片!');
    return false;
  }

  if (file.size / 1024 / 1024 > 2) {
    ElMessage.error('图片必须小于2MB!');
    return false;
  }

  // 创建原图的URL
  originalImageUrl.value = URL.createObjectURL(file);
  return false; // 阻止自动上传
};

// 预览图片
const handlePreview = async (file: UploadFile) => {
  if (!file.url && !file.raw) {
    return;
  }
  previewImage.value = file.url || URL.createObjectURL(file.raw!);
  previewVisible.value = true;
  previewTitle.value = file.name || '';
};

// 获取风格名称
const getStyleName = (styleType: StyleType | undefined): string => {
  if (!styleType) return '';
  return styleMap[styleType] || styleType;
};

// 处理风格转换
const handleStyleConversion = async () => {
  if (fileList.value.length === 0) {
    ElMessage.error('请先上传图片');
    return;
  }
  if (!formState.styleType) {
    ElMessage.error('请选择艺术风格');
    return;
  }

  try {
    converting.value = true;
    ElMessage({
      message: '正在转换风格，请稍候...',
      type: 'info',
      duration: 0,
      showClose: true,
      grouping: true,
    });

    // 获取文件对象
    const file = fileList.value[0].raw;

    // 创建FormData对象
    const formData = new FormData();
    formData.append('image', file || new Blob());
    formData.append('style', formState.styleType);

    // 模拟API调用
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // 模拟响应结果（使用原图模拟）
    resultImage.value = originalImageUrl.value;

    ElMessage.closeAll();
    ElMessage.success('风格转换成功!');
  } catch (error) {
    console.error('风格转换失败:', error);
    ElMessage.closeAll();
    ElMessage.error('风格转换失败，请重试');
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

  ElMessage.success('图片下载开始');
};

// 重置表单
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

.upload-tip {
  font-size: 12px;
  color: #999;
  margin-top: 8px;
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
