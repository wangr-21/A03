<template>
  <el-card header="智能教案生成">
    <el-form
      :model="formState"
      @submit.prevent="handleGenerateLesson"
      label-position="top"
    >
      <el-form-item label="学科" prop="subject" :rules="[{ required: true, message: '请选择学科' }]">
        <el-select v-model="formState.subject" placeholder="请选择学科" style="width: 100%">
          <el-option 
            v-for="item in subjects" 
            :key="item.value" 
            :label="item.label" 
            :value="item.value"
          />
        </el-select>
      </el-form-item>
      
      <el-form-item label="年级" prop="grade" :rules="[{ required: true, message: '请选择年级' }]">
        <el-select v-model="formState.grade" placeholder="请选择年级" style="width: 100%">
          <el-option 
            v-for="item in grades" 
            :key="item.value" 
            :label="item.label" 
            :value="item.value" 
          />
        </el-select>
      </el-form-item>
      
      <el-form-item 
        label="教学内容" 
        prop="chapter"
        :rules="[{ required: true, message: '请输入教学内容' }]"
      >
        <el-input
          v-model="formState.chapter"
          type="textarea"
          :rows="4"
          placeholder="请输入教学内容"
        />
      </el-form-item>
      
      <el-form-item 
        label="教学目标"
        prop="objectives"
        :rules="[{ required: true, message: '请输入教学目标' }]"
      >
        <el-input
          v-model="formState.objectives"
          type="textarea"
          :rows="4"
          placeholder="请输入教学目标"
        />
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" native-type="submit">生成教案</el-button>
      </el-form-item>
    </el-form>
    
    <el-card v-if="lessonPlan" header="生成的教案" style="margin-top: 16px">
      <pre style="white-space: pre-wrap">{{ lessonPlan }}</pre>
    </el-card>
  </el-card>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { ElMessage } from 'element-plus';
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

const handleGenerateLesson = async (_values: LessonPlan) => {
  try {
    ElMessage({
      message: '正在生成教案...',
      type: 'info',
      duration: 0,
      showClose: true,
      grouping: true
    });
    
    const response = await api.generateTeachingPlan({
      subject: formState.subject || '',
      grade: formState.grade || '',
      topic: formState.chapter || '',
    });

    if (response.success) {
      ElMessage.closeAll();
      ElMessage.success('教案生成成功！');
      lessonPlan.value = response.data;
    } else {
      throw new Error('生成教案失败');
    }
  } catch (error: any) {
    ElMessage.closeAll();
    ElMessage.error('生成教案失败，请重试');
    console.error('生成教案错误:', error);
  }
};
</script>