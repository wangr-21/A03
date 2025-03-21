<template>
  <a-card title="互动环节设计">
    <a-form layout="vertical" @finish="handleGenerateActivity">
      <a-form-item name="activityType" label="互动类型">
        <a-select placeholder="请选择互动类型">
          <a-select-option value="discussion">分组讨论</a-select-option>
          <a-select-option value="game">教学游戏</a-select-option>
          <a-select-option value="quiz">课堂测验</a-select-option>
        </a-select>
      </a-form-item>
      <a-form-item name="duration" label="时长(分钟)">
        <a-input type="number" />
      </a-form-item>
      <a-form-item name="description" label="活动描述">
        <a-textarea :rows="4" placeholder="请描述互动活动的具体内容"></a-textarea>
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit">生成互动方案</a-button>
      </a-form-item>
    </a-form>
    <a-card v-if="activityPlan" title="生成的互动方案" style="margin-top: 16px">
      <pre style="white-space: pre-wrap">{{ activityPlan }}</pre>
    </a-card>
  </a-card>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { message } from 'ant-design-vue';

const activityPlan = ref('');

const handleGenerateActivity = async (values: any) => {
  try {
    message.loading({ content: '正在生成互动方案...', key: 'activityPlan' });
    // 模拟API调用
    setTimeout(() => {
      activityPlan.value = `
# ${
        values.activityType === 'discussion'
          ? '分组讨论'
          : values.activityType === 'game'
          ? '教学游戏'
          : '课堂测验'
      }活动方案

## 活动时长
${values.duration || 15}分钟

## 活动描述
${values.description || '默认活动描述'}

## 活动流程
1. 准备阶段 (3分钟)
2. 活动执行 (${(values.duration || 15) - 5}分钟)
3. 总结反馈 (2分钟)
      `;
      message.success({ content: '互动方案生成成功！', key: 'activityPlan' });
    }, 1500);
  } catch (error) {
    message.error({ content: '生成互动方案失败，请重试', key: 'activityPlan' });
    console.error('生成互动方案错误:', error);
  }
};
</script>
