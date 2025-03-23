<template>
  <el-card header="互动环节设计">
    <el-form label-position="top" @submit.prevent="handleGenerateActivity">
      <el-form-item label="互动类型">
        <el-select v-model="formData.activityType" placeholder="请选择互动类型" style="width: 25%">
          <el-option label="分组讨论" value="discussion" />
          <el-option label="教学游戏" value="game" />
          <el-option label="课堂测验" value="quiz" />
        </el-select>
      </el-form-item>

      <el-form-item label="时长(分钟)">
        <el-input-number v-model="formData.duration" :min="1" :max="120" style="width: 15%" />
      </el-form-item>

      <el-form-item label="活动描述">
        <el-input
          v-model="formData.description"
          type="textarea"
          :rows="4"
          placeholder="请描述互动活动的具体内容"
        />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" native-type="submit">生成互动方案</el-button>
      </el-form-item>
    </el-form>

    <el-card v-if="activityPlan" header="生成的互动方案" style="margin-top: 16px">
      <pre style="white-space: pre-wrap">{{ activityPlan }}</pre>
    </el-card>
  </el-card>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { ElMessage } from 'element-plus';

const activityPlan = ref('');
const formData = reactive({
  activityType: '',
  duration: 15,
  description: '',
});

const handleGenerateActivity = async () => {
  try {
    ElMessage({
      message: '正在生成互动方案...',
      type: 'info',
      duration: 0,
      showClose: true,
      grouping: true,
    });

    // 模拟API调用
    setTimeout(() => {
      activityPlan.value = `
# ${
        formData.activityType === 'discussion'
          ? '分组讨论'
          : formData.activityType === 'game'
          ? '教学游戏'
          : '课堂测验'
      }活动方案

## 活动时长
${formData.duration || 15}分钟

## 活动描述
${formData.description || '默认活动描述'}

## 活动流程
1. 准备阶段 (3分钟)
2. 活动执行 (${(formData.duration || 15) - 5}分钟)
3. 总结反馈 (2分钟)
      `;

      ElMessage.closeAll();
      ElMessage.success('互动方案生成成功！');
    }, 1500);
  } catch (error) {
    ElMessage.closeAll();
    ElMessage.error('生成互动方案失败，请重试');
    console.error('生成互动方案错误:', error);
  }
};
</script>
