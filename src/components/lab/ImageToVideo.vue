<script setup lang="ts">
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import type { UploadUserFile } from 'element-plus';
import { generateVideo } from '@/api';
import ImageUploader from './ImageUploader.vue';

// --- State for Image to Video ---
const imageToVideoFile = ref<UploadUserFile | null>(null);
const imageToVideoImageUrl = ref<string>('');
const isGeneratingVideo = ref<boolean>(false);
const generatedVideoUrl = ref<string>('');
const selectedMusic = ref<string>(''); // Music selection
const videoScript = ref<string>(''); // Generated script
const showVideoPlayerDialog = ref<boolean>(false);

// Upload handler
const handleVideoUploadSuccess = (url: string, file: UploadUserFile ) => {
  imageToVideoImageUrl.value = url;
  imageToVideoFile.value = file;
  generatedVideoUrl.value = ''; // Clear previous result
  videoScript.value = '';
};

// Generate video
const generateVideoFunc = async (): Promise<void> => {
  if (!imageToVideoFile.value) {
    ElMessage.warning('请先上传图片！');
    return;
  }
  isGeneratingVideo.value = true;
  generatedVideoUrl.value = '';
  videoScript.value = '';

  try {
    const result = await generateVideo(imageToVideoFile.value, selectedMusic.value);
    generatedVideoUrl.value = result.videoUrl;
    videoScript.value = result.script;
    ElMessage.success('视频生成成功！');
  } catch (error) {
    console.error('Error generating video:', error);
    ElMessage.error('视频生成失败，请稍后重试');
  } finally {
    isGeneratingVideo.value = false;
  }
};

// Download generated video
const downloadVideo = () => {
  if (!generatedVideoUrl.value) return;

  const link = document.createElement('a');
  link.href = generatedVideoUrl.value;
  link.download = `video_${Date.now()}.mp4`;
  link.click();
};
</script>

<template>
  <el-card class="tool-panel">
    <el-row :gutter="30">
      <!-- Left: Upload & Settings -->
      <el-col :span="8">
        <ImageUploader
          title="1. 上传静态图片"
          @upload-success="handleVideoUploadSuccess"
        />
        <div class="image-preview" v-if="imageToVideoImageUrl">
          <h5>图片预览</h5>
          <el-image :src="imageToVideoImageUrl" fit="contain"></el-image>
        </div>
        <el-form label-position="top" style="margin-top: 20px">
          <el-form-item label="选择背景音乐">
            <el-select v-model="selectedMusic" placeholder="选择音乐(可选)" clearable>
              <el-option label="轻快节奏" value="music1.mp3"></el-option>
              <el-option label="舒缓旋律" value="music2.mp3"></el-option>
              <el-option label="史诗氛围" value="music3.mp3"></el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <el-button
          type="primary"
          @click="generateVideoFunc"
          :disabled="!imageToVideoImageUrl || isGeneratingVideo"
          :loading="isGeneratingVideo"
          class="action-button"
          icon="VideoPlay"
        >
          {{ isGeneratingVideo ? '正在生成...' : '开始生成视频' }}
        </el-button>
      </el-col>

      <!-- Right: Result & Script -->
      <el-col :span="16">
        <h4>2. 生成结果</h4>
        <div
          class="video-results"
          v-loading="isGeneratingVideo"
          element-loading-text="正在生成视频..."
        >
          <div v-if="generatedVideoUrl">
            <h5>视频预览</h5>
            <div class="video-player-placeholder" @click="showVideoPlayerDialog = true">
              <el-icon><VideoCameraFilled /></el-icon>
              <span>点击播放视频</span>
            </div>
            <h5>智能推荐脚本</h5>
            <el-input type="textarea" :rows="4" v-model="videoScript" readonly></el-input>
            <div class="result-actions">
              <el-button type="primary" icon="Download" @click="downloadVideo">下载视频</el-button>
            </div>
          </div>
          <el-empty v-else description="请上传图片后点击开始生成"></el-empty>
        </div>
      </el-col>
    </el-row>
  </el-card>

  <!-- Video Player Dialog -->
  <el-dialog v-model="showVideoPlayerDialog" title="视频预览" width="70%" destroy-on-close>
    <video
      v-if="generatedVideoUrl"
      :src="generatedVideoUrl"
      controls
      autoplay
      style="width: 100%; max-height: 70vh"
    >
      您的浏览器不支持 Video 标签。
    </video>
  </el-dialog>
</template>

<style scoped>
.tool-panel {
  padding: 20px;
}

.tool-panel h4 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 15px;
  color: #333;
}

.image-preview {
  margin-top: 15px;
  border: 1px solid #eee;
  padding: 10px;
  border-radius: 4px;
  min-height: 150px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.image-preview h5 {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}
.image-preview .el-image {
  max-width: 100%;
  max-height: 300px;
}

.action-button {
  margin-top: 20px;
  width: 100%;
}

.video-results {
  min-height: 300px;
  padding-top: 10px;
}
.video-player-placeholder {
  height: 250px;
  background-color: #f0f2f5;
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #909399;
  transition: background-color 0.3s ease;
  margin-bottom: 15px;
}
.video-player-placeholder:hover {
  background-color: #e4e7ed;
}
.video-player-placeholder .el-icon {
  font-size: 50px;
  margin-bottom: 10px;
}
.result-actions {
  margin-top: 15px;
  text-align: center;
}
</style>
