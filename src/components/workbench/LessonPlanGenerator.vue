<template>
  <a-card title="智能教案生成">
    <a-form
      layout="vertical"
      @finish="handleGenerateLesson"
      :model="formState"
      :validate-trigger="['submit']"
    >
      <a-form-item name="subject" label="学科" :rules="[{ required: true, message: '请选择学科' }]">
        <a-select v-model:value="formState.subject" placeholder="请选择学科">
          <a-select-option v-for="item in subjects" :key="item.value" :value="item.value">
            {{ item.label }}
          </a-select-option>
        </a-select>
      </a-form-item>
      <a-form-item name="grade" label="年级" :rules="[{ required: true, message: '请选择年级' }]">
        <a-select v-model:value="formState.grade" placeholder="请选择年级">
          <a-select-option v-for="item in grades" :key="item.value" :value="item.value">
            {{ item.label }}
          </a-select-option>
        </a-select>
      </a-form-item>
      <a-form-item
        name="chapter"
        label="教学内容"
        :rules="[{ required: true, message: '请输入教学内容' }]"
      >
        <a-textarea v-model:value="formState.chapter" :rows="4" placeholder="请输入教学内容" />
      </a-form-item>
      <a-form-item
        name="objectives"
        label="教学目标"
        :rules="[{ required: true, message: '请输入教学目标' }]"
      >
        <a-textarea v-model:value="formState.objectives" :rows="4" placeholder="请输入教学目标" />
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
import { ref, reactive } from 'vue';
import { message } from 'ant-design-vue';
import api from '@/api';

const lessonPlan = ref<string | undefined>(undefined);
const formState = reactive({
  subject: undefined as string | undefined,
  grade: undefined as string | undefined,
  chapter: undefined as string | undefined,
  objectives: undefined as string | undefined,
});

const subjects = [
  { label: '语文', value: 'chinese' },
  { label: '数学', value: 'math' },
  { label: '英语', value: 'english' },
];
const grades = [
  { label: '初一', value: '7' },
  { label: '初二', value: '8' },
  { label: '初三', value: '9' },
];

interface LessonPlan {
  subject: string;
  grade: string;
  chapter: string;
  objectives: string;
}

const handleGenerateLesson = async (values: LessonPlan) => {
  try {
    message.loading({ content: '正在生成教案...', key: 'lessonPlan' });
    const response = await api.generateTeachingPlan({
      subject: values.subject,
      grade: values.grade,
      topic: values.chapter,
    });

    if (response.success) {
      message.success({ content: '教案生成成功！', key: 'lessonPlan' });
      lessonPlan.value = response.data;
    } else {
      throw new Error('生成教案失败');
    }
  } catch (error: any) {
    message.error({ content: '生成教案失败，请重试', key: 'lessonPlan' });
    console.error('生成教案错误:', error);
  }
};
</script>
