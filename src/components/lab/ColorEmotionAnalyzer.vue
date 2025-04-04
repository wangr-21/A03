<script setup lang="ts">
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import type { UploadUserFile } from 'element-plus';
import { analyzeColorEmotion } from '@/api';
import type { ColorAnalysisResultType } from '@/api';
import ImageUploader from './ImageUploader.vue';
import ColorRadarChart from './ColorRadarChart.vue';

// --- State for Color Emotion Analysis ---
const colorAnalysisFile = ref<UploadUserFile | null>(null);
const colorAnalysisImageUrl = ref<string>('');
const isAnalyzingColor = ref<boolean>(false);
const colorAnalysisResult = ref<ColorAnalysisResultType | null>(null);

// Upload handler
const handleColorUploadSuccess = (result: { url: string; file: UploadUserFile }) => {
  colorAnalysisImageUrl.value = result.url;
  colorAnalysisFile.value = result.file;
  colorAnalysisResult.value = null; // Clear previous result
};

// Analyze color emotion
const analyzeColorEmotionFunc = async (): Promise<void> => {
  if (!colorAnalysisFile.value) {
    ElMessage.warning('请先上传图片！');
    return;
  }
  isAnalyzingColor.value = true;
  colorAnalysisResult.value = null;
  console.log('Analyzing color for file:', colorAnalysisFile.value.name);

  try {
    colorAnalysisResult.value = await analyzeColorEmotion(colorAnalysisFile.value);
    ElMessage.success('色彩情感分析完成！');
  } catch (error) {
    console.error('Error analyzing color:', error);
    ElMessage.error('色彩分析失败，请稍后重试');
  } finally {
    isAnalyzingColor.value = false;
  }
};
</script>

<template>
  <el-card class="tool-panel">
    <el-row :gutter="30">
      <!-- Left: Upload & Image -->
      <el-col :span="8">
        <ImageUploader
          title="1. 上传作品图片"
          @upload-success="handleColorUploadSuccess"
        />
        <div class="image-preview" v-if="colorAnalysisImageUrl">
          <h5>作品预览</h5>
          <el-image :src="colorAnalysisImageUrl" fit="contain"></el-image>
        </div>
        <el-button
          type="primary"
          @click="analyzeColorEmotionFunc"
          :disabled="!colorAnalysisImageUrl || isAnalyzingColor"
          :loading="isAnalyzingColor"
          class="action-button"
          icon="Brush"
        >
          {{ isAnalyzingColor ? '正在分析...' : '开始色彩分析' }}
        </el-button>
      </el-col>

      <!-- Right: Analysis Results -->
      <el-col :span="16">
        <h4>2. 色彩情感分析结果</h4>
        <div
          class="analysis-results"
          v-loading="isAnalyzingColor"
          element-loading-text="正在分析色彩情感..."
        >
          <div v-if="colorAnalysisResult">
            <el-row :gutter="20">
              <el-col :span="12">
                <h5>色彩维度雷达图</h5>
                <ColorRadarChart :chart-data="colorAnalysisResult.radarData" />
              </el-col>
              <el-col :span="12">
                <h5>主要色彩</h5>
                <div class="dominant-colors">
                  <span
                    v-for="color in colorAnalysisResult.dominantColors"
                    :key="color"
                    :style="{ backgroundColor: color }"
                    class="color-swatch"
                  ></span>
                </div>
                <h5>情感关键词</h5>
                <div class="keyword-cloud">
                  <el-tag
                    v-for="word in colorAnalysisResult.keywords"
                    :key="word"
                    style="margin: 4px"
                    >{{ word }}</el-tag
                  >
                </div>
              </el-col>
            </el-row>
          </div>
          <el-empty v-else description="请上传图片并点击开始分析"></el-empty>
        </div>
      </el-col>
    </el-row>
  </el-card>
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

.analysis-results {
  min-height: 300px;
  padding-top: 10px;
}
.analysis-results h5 {
  font-size: 15px;
  margin-bottom: 10px;
  color: #444;
}
.dominant-colors {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}
.color-swatch {
  width: 30px;
  height: 30px;
  border-radius: 4px;
  border: 1px solid #eee;
}
.keyword-cloud {
  padding: 10px;
  background-color: #f8f8f8;
  border-radius: 4px;
}
</style>
