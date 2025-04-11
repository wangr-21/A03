<script setup lang="ts">
interface Hotspot {
  image: string;
  description?: string; // 添加画作简介字段
}

import hotspotImage from '@/assets/demo/hotspot.png';
import { ref } from 'vue';

// 热点数据
const hotspot: Hotspot = {
  image: hotspotImage,
  description:
    '《日出·印象》是法国印象派画家克劳德·莫奈于1872年创作的油画作品。这幅画描绘了法国勒阿弗尔港口日出时分的景象，以独特的光影效果和笔触表现了印象派的艺术特色。这幅作品也是"印象派"名称的由来，对现代艺术产生了深远影响。',
};

// 控制对话框显示
const dialogVisible = ref(false);

// 点击图片显示详情
const showImageDetail = (): void => {
  dialogVisible.value = true;
  console.log('Show image detail');
};
</script>

<template>
  <el-card class="hotspot-card">
    <template #header>
      <div class="card-header">
        <h3>
          <el-icon><DataLine /></el-icon> 今日名画推荐
        </h3>
      </div>
    </template>
    <div class="hotspot-content">
      <div class="image-container" @click="showImageDetail">
        <img :src="hotspot.image" alt="今日名画推荐" class="hotspot-image" />
        <div class="image-overlay">
          <el-icon><ZoomIn /></el-icon>
        </div>
      </div>
    </div>
  </el-card>

  <!-- 画作简介对话框 -->
  <el-dialog
    v-model="dialogVisible"
    title="画作简介"
    width="50%"
    :close-on-click-modal="true"
    :show-close="true"
  >
    <div class="artwork-detail">
      <img :src="hotspot.image" alt="今日名画推荐" class="artwork-image" />
      <p class="artwork-description">{{ hotspot.description }}</p>
    </div>
  </el-dialog>
</template>

<style scoped>
.hotspot-card {
  height: 360px;
  display: flex;
  flex-direction: column;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 10px;
  min-height: 20px;
}

.card-header h3 {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-header h3 .el-icon {
  color: #7353e5;
}

.hotspot-content {
  padding: 0 10px 10px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.image-container {
  flex: 1;
  overflow: hidden;
  border-radius: 4px;
  position: relative;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hotspot-image {
  width: auto;
  height: auto;
  max-width: 100%;
  max-height: 310px;
  object-fit: contain;
  transition: transform 0.3s ease;
}

/* 添加悬停效果 */
.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.image-overlay .el-icon {
  font-size: 32px;
  color: white;
}

.image-container:hover .image-overlay {
  opacity: 1;
}

.image-container:hover .hotspot-image {
  transform: scale(1.02);
}

/* 对话框内容样式 */
.artwork-detail {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.artwork-image {
  max-width: 100%;
  max-height: 400px;
  object-fit: contain;
}

.artwork-description {
  font-size: 16px;
  line-height: 1.6;
  color: #333;
  text-align: justify;
}
</style>
