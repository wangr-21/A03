<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>视频资源生成</span>
        <el-icon :size="24"><VideoCamera /></el-icon>
      </div>
    </template>

    <el-form
      :model="formState"
      ref="formRef"
      label-position="top"
      @submit.prevent="handleGenerateVideo"
    >
      <el-form-item
        label="视频类型"
        prop="videoType"
        :rules="[{ required: true, message: '请选择视频类型', trigger: 'change' }]"
      >
        <el-select
          v-model="formState.videoType"
          placeholder="请选择视频类型"
          clearable
          style="width: 100%"
        >
          <el-option label="微课视频" value="micro" />
          <el-option label="教学动画" value="animation" />
          <el-option label="实验演示" value="experiment" />
        </el-select>
      </el-form-item>

      <el-form-item
        label="视频脚本"
        prop="script"
        :rules="[{ required: true, message: '请输入视频内容脚本', trigger: 'blur' }]"
      >
        <el-input
          v-model="formState.script"
          type="textarea"
          :rows="4"
          placeholder="请输入视频内容脚本"
        ></el-input>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" native-type="submit">生成视频</el-button>
      </el-form-item>
    </el-form>

    <div class="preview-container" v-if="previewVideo">
      <h3>视频预览</h3>
      <div class="video-placeholder" v-if="isGenerating">
        <p>视频生成中...</p>
        <el-progress :percentage="generationProgress" />
      </div>
      <video v-else :src="previewVideo" controls class="preview-video"></video>
      <el-button
        type="primary"
        @click="saveGeneratedResource"
        style="margin-top: 16px"
        :disabled="isGenerating"
      >
        保存到资源库
      </el-button>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { ElMessage } from 'element-plus';
import { VideoCamera } from '@element-plus/icons-vue';
import type { FormInstance } from 'element-plus';
import type { Resource } from '@/types/resources';

const emit = defineEmits(['resource-generated']);
const formRef = ref<FormInstance>();

const handleResourceGenerated = (resource: Resource) => {
  resource.data.createdAt = new Date().toLocaleString();
  emit('resource-generated', resource);
};

// 表单状态
const formState = reactive({
  videoType: '',
  script: '',
});

const previewVideo = ref('');
const isGenerating = ref(false);
const generationProgress = ref(0);
let currentVideoData: {
  url: string;
  type: string;
  description: string;
} | null = null;

// interface VideoFormData {
//   videoType: 'micro' | 'animation' | 'experiment';
//   script: string;
// }

const handleGenerateVideo = async () => {
  await formRef.value?.validate((valid) => {
    if (!valid) return;
    generateVideo();
  });
};

const generateVideo = async () => {
  try {
    ElMessage({
      message: '正在生成视频资源...',
      type: 'info',
      duration: 0,
      showClose: true,
      grouping: true,
      // id: 'videoResource',
    });

    isGenerating.value = true;
    previewVideo.value = 'pending';

    // 模拟渐进式处理
    const interval = setInterval(() => {
      generationProgress.value += 10;
      if (generationProgress.value >= 100) {
        clearInterval(interval);
        completeVideoGeneration();
      }
    }, 800);
  } catch (error) {
    isGenerating.value = false;
    previewVideo.value = '';
    ElMessage.error('生成视频资源失败，请重试');
    console.error('生成视频资源错误:', error);
  }
};

const completeVideoGeneration = () => {
  const videoTypeLabels: Record<string, string> = {
    micro: '微课视频',
    animation: '教学动画',
    experiment: '实验演示',
  };

  // 这里应该是从API返回的真实视频URL
  // 但现在我们使用一个示例视频
  const sampleVideoUrl = 'https://www.w3schools.com/html/mov_bbb.mp4';

  isGenerating.value = false;
  previewVideo.value = sampleVideoUrl;

  ElMessage.closeAll();
  ElMessage.success('视频资源生成成功！');

  // 保存当前视频数据以供后续使用
  currentVideoData = {
    url: sampleVideoUrl,
    type: videoTypeLabels[formState.videoType] || formState.videoType,
    description: formState.script,
  };
};

const saveGeneratedResource = () => {
  if (currentVideoData) {
    handleResourceGenerated({
      type: '视频',
      data: currentVideoData,
    });
    ElMessage.success('视频已成功保存到资源库');

    // 重置预览和表单
    previewVideo.value = '';
    generationProgress.value = 0;
    currentVideoData = null;
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

.preview-video {
  max-width: 100%;
  border: 1px solid #eee;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.video-placeholder {
  padding: 40px;
  background-color: #f5f5f5;
  border-radius: 4px;
  margin-bottom: 16px;
}
</style>
