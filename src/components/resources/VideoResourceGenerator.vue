<template>
  <a-card title="视频资源生成">
    <template #extra>
      <video-camera-outlined style="font-size: 24px" />
    </template>
    <a-form
      layout="vertical"
      @finish="handleGenerateVideo"
      :model="formState"
      ref="formRef"
      :validate-trigger="['submit']"
    >
      <a-form-item
        name="videoType"
        label="视频类型"
        :rules="[{ required: true, message: '请选择视频类型' }]"
      >
        <a-select v-model:value="formState.videoType" placeholder="请选择视频类型" allow-clear>
          <a-select-option value="micro">微课视频</a-select-option>
          <a-select-option value="animation">教学动画</a-select-option>
          <a-select-option value="experiment">实验演示</a-select-option>
        </a-select>
      </a-form-item>
      <a-form-item
        name="script"
        label="视频脚本"
        :rules="[{ required: true, message: '请输入视频内容脚本' }]"
      >
        <a-textarea
          v-model:value="formState.script"
          :rows="4"
          placeholder="请输入视频内容脚本"
        ></a-textarea>
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit">生成视频</a-button>
      </a-form-item>
    </a-form>

    <div class="preview-container" v-if="previewVideo">
      <h3>视频预览</h3>
      <div class="video-placeholder" v-if="isGenerating">
        <p>视频生成中...</p>
        <a-progress :percent="generationProgress" />
      </div>
      <video v-else :src="previewVideo" controls class="preview-video"></video>
      <a-button
        type="primary"
        @click="saveGeneratedResource"
        style="margin-top: 16px"
        :disabled="isGenerating"
      >
        保存到资源库
      </a-button>
    </div>
  </a-card>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { message } from 'ant-design-vue';
import { VideoCameraOutlined } from '@ant-design/icons-vue';
import type { FormInstance } from 'ant-design-vue';
import { Resource } from '@/types/resources';

const emit = defineEmits(['resource-generated']);
const formRef = ref<FormInstance>();

const handleResourceGenerated = (resource: Resource) => {
  resource.data.createdAt = new Date().toLocaleString();
  emit('resource-generated', resource);
};

// 表单状态 - 使用 undefined 而不是空字符串
const formState = reactive({
  videoType: undefined, // 修改为 undefined
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

interface VideoFormData {
  videoType: 'micro' | 'animation' | 'experiment';
  script: string;
}

const handleGenerateVideo = async (values: VideoFormData) => {
  try {
    message.loading({ content: '正在生成视频资源...', key: 'videoResource' });
    isGenerating.value = true;
    previewVideo.value = 'pending';

    // 模拟渐进式处理
    const interval = setInterval(() => {
      generationProgress.value += 10;
      if (generationProgress.value >= 100) {
        clearInterval(interval);
        completeVideoGeneration(values);
      }
    }, 800);
  } catch (error) {
    isGenerating.value = false;
    previewVideo.value = '';
    message.error({
      content: '生成视频资源失败，请重试',
      key: 'videoResource',
    });
    console.error('生成视频资源错误:', error);
  }
};

const completeVideoGeneration = (values: VideoFormData) => {
  const videoTypeLabels = {
    micro: '微课视频',
    animation: '教学动画',
    experiment: '实验演示',
  };

  // 这里应该是从API返回的真实视频URL
  // 但现在我们使用一个示例视频
  const sampleVideoUrl = 'https://www.w3schools.com/html/mov_bbb.mp4';

  isGenerating.value = false;
  previewVideo.value = sampleVideoUrl;

  message.success({ content: '视频资源生成成功！', key: 'videoResource' });

  // 保存当前视频数据以供后续使用
  currentVideoData = {
    url: sampleVideoUrl,
    type: videoTypeLabels[values.videoType],
    description: values.script,
  };
};

const saveGeneratedResource = () => {
  if (currentVideoData) {
    handleResourceGenerated({
      type: '视频',
      data: currentVideoData,
    });
    message.success('视频已成功保存到资源库');

    // 重置预览和表单
    previewVideo.value = '';
    generationProgress.value = 0;
    currentVideoData = null;
    formRef.value?.resetFields();
  }
};
</script>

<style scoped>
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
