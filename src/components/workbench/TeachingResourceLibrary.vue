<template>
  <el-card header="教学资源库">
    <el-space direction="vertical" style="width: 100%" :size="24">
      <el-card shadow="hover" header="推荐资源">
        <p>1. 教学PPT模板</p>
        <p>2. 课堂互动游戏素材</p>
        <p>3. 知识点讲解视频</p>
        <p>4. 练习题资源包</p>
      </el-card>

      <el-card shadow="hover" header="资源生成">
        <el-space>
          <el-button @click="handleGenerateImage">生成图片资源</el-button>
          <el-button @click="handleGenerateVideo">生成视频资源</el-button>
          <el-button @click="handleGenerateExercise">生成练习题</el-button>
        </el-space>
      </el-card>
    </el-space>
  </el-card>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus';
import api from '@/api';

const handleGenerateImage = async () => {
  try {
    ElMessage({
      message: '正在生成图片...',
      type: 'info',
      duration: 0,
      showClose: true,
      grouping: true,
    });

    const response = await api.generateTeachingImage('教学相关的图片');
    if (response.success) {
      ElMessage.closeAll();
      ElMessage.success('图片生成成功！');
      // TODO: 处理生成的图片URL
    } else {
      throw new Error('生成图片失败');
    }
  } catch (error) {
    ElMessage.closeAll();
    ElMessage.error('生成图片失败，请重试');
    console.error('生成图片错误:', error);
  }
};

const handleGenerateVideo = async () => {
  ElMessage.info('视频生成功能正在开发中...');
};

const handleGenerateExercise = async () => {
  ElMessage.info('练习题生成功能正在开发中...');
};
</script>
