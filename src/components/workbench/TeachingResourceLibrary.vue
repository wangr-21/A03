<template>
  <a-card title="教学资源库">
    <a-space direction="vertical" style="width: 100%">
      <a-card type="inner" title="推荐资源">
        <p>1. 教学PPT模板</p>
        <p>2. 课堂互动游戏素材</p>
        <p>3. 知识点讲解视频</p>
        <p>4. 练习题资源包</p>
      </a-card>
      <a-card type="inner" title="资源生成">
        <a-space>
          <a-button @click="handleGenerateImage">生成图片资源</a-button>
          <a-button @click="handleGenerateVideo">生成视频资源</a-button>
          <a-button @click="handleGenerateExercise">生成练习题</a-button>
        </a-space>
      </a-card>
    </a-space>
  </a-card>
</template>

<script setup lang="ts">
import { message } from 'ant-design-vue';
import api from '@/api';

const handleGenerateImage = async () => {
  try {
    message.loading({ content: '正在生成图片...', key: 'image' });
    const response = await api.generateTeachingImage('教学相关的图片');
    if (response.success) {
      message.success({ content: '图片生成成功！', key: 'image' });
      // TODO: 处理生成的图片URL
    } else {
      throw new Error('生成图片失败');
    }
  } catch (error) {
    message.error({ content: '生成图片失败，请重试', key: 'image' });
    console.error('生成图片错误:', error);
  }
};

const handleGenerateVideo = async () => {
  message.info('视频生成功能正在开发中...');
};

const handleGenerateExercise = async () => {
  message.info('练习题生成功能正在开发中...');
};
</script>
