<script setup lang="ts">
import { ref, nextTick } from 'vue'
import {
  ElMessage,
  ElUpload,
  ElTabs,
  ElTabPane,
  ElCard,
  ElRow,
  ElCol,
  ElButton,
  ElIcon,
  ElImage,
  ElDialog,
} from 'element-plus'
import type { UploadUserFile } from 'element-plus'
import * as echarts from 'echarts'
import type { EChartsType } from 'echarts'

// --- 定义接口 ---
// 样式选项接口
interface StyleOption {
  name: string
  key: string
  thumb: string
}

// 颜色分析结果接口
interface ColorAnalysisResultType {
  radarData: number[]
  keywords: string[]
  dominantColors: string[]
}

// --- General State ---
const activeToolTab = ref<string>('styleTransfer') // To switch between tools

// 颜色分析结果接口
interface ColorAnalysisResultType {
  radarData: number[]
  keywords: string[]
  dominantColors: string[]
}

// --- 类型定义 ---
interface StyleOption {
  name: string
  key: string
  thumb: string
}

interface ColorAnalysisResultType {
  radarData: number[]
  keywords: string[]
  dominantColors: string[]
}

// --- State for Style Transfer ---
const styleTransferFile = ref<UploadUserFile | null>(null)
const styleTransferImageUrl = ref<string>('')
const styleTransferResultUrl = ref<string>('')
const availableStyles = ref<StyleOption[]>([
  { name: '印象派', key: 'impressionism', thumb: '/src/assets/style_thumb1.jpg' },
  { name: '梵高', key: 'van_gogh', thumb: '/src/assets/style_thumb2.jpg' },
  { name: '水墨画', key: 'ink_wash', thumb: '/src/assets/style_thumb3.jpg' },
  { name: '赛博朋克', key: 'cyberpunk', thumb: '/src/assets/style_thumb4.jpg' },
  { name: '浮世绘', key: 'ukiyo_e', thumb: '/src/assets/style_thumb5.jpg' },
  // Add more styles
])
const selectedStyle = ref<string>(availableStyles.value[0]?.key || '')
const isApplyingStyle = ref<boolean>(false)

// --- State for Color Emotion Analysis ---
const colorAnalysisFile = ref<UploadUserFile | null>(null)
const colorAnalysisImageUrl = ref<string>('')
const isAnalyzingColor = ref<boolean>(false)
const colorAnalysisResult = ref<ColorAnalysisResultType | null>(null)
let colorRadarChart: EChartsType | null = null

// --- State for Image to Video ---
const imageToVideoFile = ref<UploadUserFile | null>(null)
const imageToVideoImageUrl = ref<string>('')
const isGeneratingVideo = ref<boolean>(false)
const generatedVideoUrl = ref<string>('')
const selectedMusic = ref<string>('') // Music selection
const videoScript = ref<string>('') // Generated script
const showVideoPlayerDialog = ref<boolean>(false)

// --- Upload Handlers (Common Logic Can Be Extracted) ---
interface UploadResponse {
  success: boolean
  url?: string
  message?: string
}

const handleStyleUploadSuccess = (response: UploadResponse, uploadFile: UploadUserFile): void => {
  console.log('Style Image Upload Success:', response)
  styleTransferImageUrl.value = URL.createObjectURL(uploadFile.raw!)
  styleTransferFile.value = uploadFile
  styleTransferResultUrl.value = '' // Clear previous result
}

const handleColorUploadSuccess = (response: UploadResponse, uploadFile: UploadUserFile): void => {
  console.log('Color Image Upload Success:', response)
  colorAnalysisImageUrl.value = URL.createObjectURL(uploadFile.raw!)
  colorAnalysisFile.value = uploadFile
  colorAnalysisResult.value = null // Clear previous result
}

const handleVideoUploadSuccess = (response: UploadResponse, uploadFile: UploadUserFile): void => {
  console.log('Video Image Upload Success:', response)
  imageToVideoImageUrl.value = URL.createObjectURL(uploadFile.raw!)
  imageToVideoFile.value = uploadFile
  generatedVideoUrl.value = '' // Clear previous result
}

const handleUploadError = (
  error: Error,
  uploadFile: UploadUserFile,
  uploadFiles: UploadUserFile[],
): void => {
  ElMessage.error('图片上传失败!')
  console.error('Upload Error:', error)
}

const beforeUpload = (rawFile: File): boolean | Promise<File> => {
  if (!rawFile.type.startsWith('image/')) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (rawFile.size / 1024 / 1024 > 5) {
    // Limit size to 5MB
    ElMessage.error('图片大小不能超过 5MB!')
    return false
  }
  return true
}

// --- Tool Logic Functions (Placeholders) ---
const applyStyleTransfer = async (): Promise<void> => {
  if (!styleTransferFile.value || !selectedStyle.value) {
    ElMessage.warning('请先上传图片并选择风格！')
    return
  }
  isApplyingStyle.value = true
  console.log('Applying style:', selectedStyle.value, 'to file:', styleTransferFile.value.name)
  // Simulate API call
  await new Promise((resolve) => setTimeout(resolve, 3000))
  // Replace with actual API call, response should contain the result image URL
  styleTransferResultUrl.value = '/src/assets/styled_result.jpg' // Placeholder result
  isApplyingStyle.value = false
  ElMessage.success('风格转换成功！')
}

const analyzeColorEmotion = async (): Promise<void> => {
  if (!colorAnalysisFile.value) {
    ElMessage.warning('请先上传图片！')
    return
  }
  isAnalyzingColor.value = true
  colorAnalysisResult.value = null
  console.log('Analyzing color for file:', colorAnalysisFile.value.name)
  // Simulate API call
  await new Promise((resolve) => setTimeout(resolve, 2000))
  // Replace with actual API call, response should contain analysis data
  colorAnalysisResult.value = {
    radarData: [80, 60, 75, 50, 90], // Example: Warmth, Brightness, Contrast, Saturation, Harmony
    keywords: ['活泼', '明亮', '温暖', '积极', '对比强烈'],
    dominantColors: ['#FF7A5A', '#FFB64D', '#FFFFFF', '#7353E5'],
  }
  isAnalyzingColor.value = false
  ElMessage.success('色彩情感分析完成！')
  // Initialize or update the radar chart
  nextTick(initColorRadarChart)
}

const generateVideo = async (): Promise<void> => {
  if (!imageToVideoFile.value) {
    ElMessage.warning('请先上传图片！')
    return
  }
  isGeneratingVideo.value = true
  generatedVideoUrl.value = ''
  videoScript.value = ''
  console.log('Generating video for file:', imageToVideoFile.value.name)
  // Simulate API call
  await new Promise((resolve) => setTimeout(resolve, 5000))
  // Replace with actual API call, response should contain video URL and maybe script
  generatedVideoUrl.value = '/src/assets/generated_video.mp4' // Placeholder result
  videoScript.value = `1. 画面拉近，聚焦主体。
2. 添加轻快背景音乐。
3. 元素[A]向右移动。
4. 画面淡出。`
  isGeneratingVideo.value = false
  ElMessage.success('视频生成成功！')
  showVideoPlayerDialog.value = true
}

// --- Chart Initialization (Placeholder) ---
const initColorRadarChart = (): void => {
  const chartDom = document.getElementById('colorRadarChart')
  if (!chartDom || !colorAnalysisResult.value) return
  if (colorRadarChart) colorRadarChart.dispose() // Dispose previous instance
  colorRadarChart = echarts.init(chartDom)
  const option = {
    tooltip: { trigger: 'item' },
    radar: {
      indicator: [
        { name: '暖度', max: 100 },
        { name: '亮度', max: 100 },
        { name: '对比度', max: 100 },
        { name: '饱和度', max: 100 },
        { name: '和谐度', max: 100 },
      ],
    },
    series: [
      {
        name: '色彩分析',
        type: 'radar',
        data: [{ value: colorAnalysisResult.value.radarData, name: '分析结果' }],
      },
    ],
  }
  colorRadarChart.setOption(option)
}
</script>

<template>
  <div class="lab-container">
    <div class="page-header">
      <h1 class="page-title">幻画实验室</h1>
      <!-- General Upload might be removed if each tool has its own -->
    </div>

    <el-tabs v-model="activeToolTab" class="tool-tabs">
      <el-tab-pane label="风格万花筒" name="styleTransfer">
        <el-card class="tool-panel">
          <el-row :gutter="30">
            <!-- Left: Upload & Original Image -->
            <el-col :span="10">
              <h4>1. 上传原始图片</h4>
              <el-upload
                class="image-uploader"
                action="/api/upload"
                :show-file-list="false"
                :on-success="handleStyleUploadSuccess"
                :on-error="handleUploadError"
                :before-upload="beforeUpload"
                drag
              >
                <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                <div class="el-upload__text">
                  拖拽文件到此处 或 <em>点击上传</em> (JPG/PNG, &lt;5MB)
                </div>
              </el-upload>
              <div class="image-preview" v-if="styleTransferImageUrl">
                <h5>原图预览</h5>
                <el-image :src="styleTransferImageUrl" fit="contain"></el-image>
              </div>
            </el-col>

            <!-- Middle: Style Selection -->
            <el-col :span="4">
              <h4>2. 选择艺术风格</h4>
              <div class="style-selector">
                <div
                  v-for="style in availableStyles"
                  :key="style.key"
                  class="style-option"
                  :class="{ 'is-active': selectedStyle === style.key }"
                  @click="selectedStyle = style.key"
                >
                  <el-image :src="style.thumb" fit="cover"></el-image>
                  <span>{{ style.name }}</span>
                </div>
              </div>
            </el-col>

            <!-- Right: Result & Action -->
            <el-col :span="10">
              <h4>3. 生成风格化图片</h4>
              <div
                class="result-area"
                v-loading="isApplyingStyle"
                element-loading-text="正在应用风格..."
              >
                <div class="image-preview result-preview" v-if="styleTransferResultUrl">
                  <h5>效果预览</h5>
                  <el-image :src="styleTransferResultUrl" fit="contain"></el-image>
                  <div class="result-actions">
                    <el-button type="primary" icon="Download">下载图片</el-button>
                  </div>
                </div>
                <el-empty v-else description="请上传图片并选择风格后点击生成"></el-empty>
              </div>
              <el-button
                type="primary"
                @click="applyStyleTransfer"
                :disabled="!styleTransferImageUrl || !selectedStyle || isApplyingStyle"
                :loading="isApplyingStyle"
                class="action-button"
                icon="MagicStick"
              >
                {{ isApplyingStyle ? '正在转换...' : '开始风格转换' }}
              </el-button>
            </el-col>
          </el-row>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="情绪色谱仪" name="colorEmotion">
        <el-card class="tool-panel">
          <el-row :gutter="30">
            <!-- Left: Upload & Image -->
            <el-col :span="8">
              <h4>1. 上传作品图片</h4>
              <el-upload
                class="image-uploader"
                action="/api/upload"
                :show-file-list="false"
                :on-success="handleColorUploadSuccess"
                :on-error="handleUploadError"
                :before-upload="beforeUpload"
                drag
              >
                <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                <div class="el-upload__text">拖拽或点击上传</div>
              </el-upload>
              <div class="image-preview" v-if="colorAnalysisImageUrl">
                <h5>作品预览</h5>
                <el-image :src="colorAnalysisImageUrl" fit="contain"></el-image>
              </div>
              <el-button
                type="primary"
                @click="analyzeColorEmotion"
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
                      <div id="colorRadarChart" style="height: 300px"></div>
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
                      <!-- TODO: Implement Word Cloud Component -->
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
      </el-tab-pane>

      <el-tab-pane label="绘影工场" name="imageToVideo">
        <el-card class="tool-panel">
          <el-row :gutter="30">
            <!-- Left: Upload & Settings -->
            <el-col :span="8">
              <h4>1. 上传静态图片</h4>
              <el-upload
                class="image-uploader"
                action="/api/upload"
                :show-file-list="false"
                :on-success="handleVideoUploadSuccess"
                :on-error="handleUploadError"
                :before-upload="beforeUpload"
                drag
              >
                <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                <div class="el-upload__text">拖拽或点击上传</div>
              </el-upload>
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
                <!-- Add more settings like animation style if needed -->
              </el-form>
              <el-button
                type="primary"
                @click="generateVideo"
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
                    <el-button type="primary" icon="Download">下载视频</el-button>
                  </div>
                </div>
                <el-empty v-else description="请上传图片后点击开始生成"></el-empty>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-tab-pane>
    </el-tabs>

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

    <!-- Remove or Keep Existing Recent Works/Styles Section -->
    <!--
    <div class="recent-section">...</div>
    <div class="styles-section">...</div>
    -->
  </div>
</template>

<style scoped>
.lab-container {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: bold;
}

.tool-tabs {
  margin-bottom: 20px;
}

.tool-panel {
  padding: 20px;
}

.tool-panel h4 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 15px;
  color: #333;
}

.image-uploader {
  margin-bottom: 15px;
  border: 2px dashed var(--el-border-color);
  border-radius: 6px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.3s ease;
}
.image-uploader:hover {
  border-color: var(--el-color-primary);
}

.image-preview {
  margin-top: 15px;
  border: 1px solid #eee;
  padding: 10px;
  border-radius: 4px;
  min-height: 150px; /* Ensure some height even before image loads */
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
  max-height: 300px; /* Limit preview height */
}

.action-button {
  margin-top: 20px;
  width: 100%;
}

/* Style Transfer Specific */
.style-selector {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: 400px; /* Allow scrolling for many styles */
  overflow-y: auto;
}
.style-option {
  border: 2px solid transparent;
  padding: 5px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}
.style-option.is-active {
  border-color: var(--el-color-primary);
  background-color: var(--el-color-primary-light-9);
}
.style-option:hover {
  background-color: #f5f7fa;
}
.style-option .el-image {
  width: 80px;
  height: 80px;
  border-radius: 4px;
  margin-bottom: 5px;
}
.style-option span {
  font-size: 13px;
  color: #333;
}

.result-area {
  border: 1px dashed #dcdfe6;
  border-radius: 6px;
  min-height: 300px; /* Match image preview height */
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 15px;
}
.result-preview {
  border: none;
  padding: 0;
  margin-top: 0;
}
.result-actions {
  margin-top: 15px;
  text-align: center;
}

/* Color Emotion Specific */
.analysis-results {
  min-height: 300px; /* Ensure height for loading/empty state */
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
  /* Placeholder - Requires a dedicated word cloud library */
  padding: 10px;
  background-color: #f8f8f8;
  border-radius: 4px;
}

/* Image to Video Specific */
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
</style>

// --- Remove existing script block with hardcoded data --- //
<script lang="ts">
// export default {
//   data() { ... }
// }
//
</script>
