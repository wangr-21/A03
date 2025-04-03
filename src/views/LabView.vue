<script setup lang="ts">
import { ref } from 'vue';
import StyleTransfer from '@/components/lab/StyleTransfer.vue';
import ColorEmotionAnalyzer from '@/components/lab/ColorEmotionAnalyzer.vue';
import ImageToVideo from '@/components/lab/ImageToVideo.vue';

// --- General State ---
const activeToolTab = ref<string>('styleTransfer'); // To switch between tools
</script>

<template>
  <div class="lab-container">
    <div class="page-header">
      <h1 class="page-title">幻画实验室</h1>
    </div>

    <el-tabs v-model="activeToolTab" class="tool-tabs">
      <el-tab-pane label="风格万花筒" name="styleTransfer">
        <StyleTransfer />
      </el-tab-pane>

      <el-tab-pane label="情绪色谱仪" name="colorEmotion">
        <ColorEmotionAnalyzer />
      </el-tab-pane>

      <el-tab-pane label="绘影工场" name="imageToVideo">
        <ImageToVideo />
      </el-tab-pane>
    </el-tabs>
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
</style>
