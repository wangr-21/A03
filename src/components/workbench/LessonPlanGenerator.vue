<template>
  <a-card title="智能教案生成">
    <a-form layout="vertical" @finish="handleGenerateLesson">
      <a-form-item name="subject" label="学科" :rules="[{ required: true, message: '请选择学科' }]">
        <a-select placeholder="请选择学科">
          <a-select-option value="chinese">语文</a-select-option>
          <a-select-option value="math">数学</a-select-option>
          <a-select-option value="english">英语</a-select-option>
        </a-select>
      </a-form-item>
      <a-form-item name="grade" label="年级" :rules="[{ required: true, message: '请选择年级' }]">
        <a-select placeholder="请选择年级">
          <a-select-option value="7">初一</a-select-option>
          <a-select-option value="8">初二</a-select-option>
          <a-select-option value="9">初三</a-select-option>
        </a-select>
      </a-form-item>
      <a-form-item
        name="chapter"
        label="教学内容"
        :rules="[{ required: true, message: '请输入教学内容' }]"
      >
        <a-textarea :rows="4" placeholder="请输入本节课的教学内容"></a-textarea>
      </a-form-item>
      <a-form-item
        name="objectives"
        label="教学目标"
        :rules="[{ required: true, message: '请输入教学目标' }]"
      >
        <a-textarea :rows="4" placeholder="请输入教学目标"></a-textarea>
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit">生成教案</a-button>
      </a-form-item>
    </a-form>
    <a-card v-if="lessonPlan" title="生成的教案" style="margin-top: 16px">
      <pre style="white-space: pre-wrap">{{ lessonPlan }}</pre>
    </a-card>
  </a-card>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { message } from 'ant-design-vue';
import api from '@/api';

const lessonPlan = ref('');

const handleGenerateLesson = async (values: { subject: string; grade: string; topic: string }) => {
  try {
    message.loading({ content: '正在生成教案...', key: 'lessonPlan' });
    const response = await api.generateTeachingPlan(values);

    if (response.success) {
      message.success({ content: '教案生成成功！', key: 'lessonPlan' });
      lessonPlan.value = response.data;
    } else {
      throw new Error('生成教案失败');
    }
  } catch (error) {
    message.error({ content: '生成教案失败，请重试', key: 'lessonPlan' });
    console.error('生成教案错误:', error);
  }
};
</script>
