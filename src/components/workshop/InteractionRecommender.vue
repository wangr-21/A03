<script setup lang="ts">
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import MarkdownIt from 'markdown-it';
import { getRecommendedInteractions } from '@/api';
import type { InteractionItem } from '@/api';

const md = new MarkdownIt();

// Refs
const recommendedInteractions = ref<InteractionItem[]>([]);
const isLoadingInteractions = ref<boolean>(false);
const showTopicDialog = ref<boolean>(false);
const topicInput = ref<string>('');

// 打开主题输入对话框
const openTopicDialog = () => {
  showTopicDialog.value = true;
  topicInput.value = ''; // 清空输入
};

// 处理对话框确认
const handleTopicConfirm = async () => {
  if (!topicInput.value.trim()) {
    ElMessage.warning('请输入主题');
    return;
  }

  showTopicDialog.value = false;
  await fetchRecommendedInteractions(topicInput.value);
};

// 获取推荐互动
const fetchRecommendedInteractions = async (topic: string): Promise<void> => {
  isLoadingInteractions.value = true;
  recommendedInteractions.value = [];

  try {
    const response = await getRecommendedInteractions(topic);
    recommendedInteractions.value = response;
    ElMessage.success('互动推荐获取成功！');
  } catch (error) {
    console.error('Error fetching interactions:', error);
    ElMessage.error('获取互动推荐失败，请稍后重试。');
  } finally {
    isLoadingInteractions.value = false;
  }
};
</script>

<template>
  <el-card class="interactions-card">
    <!-- 卡片头部 -->
    <template #header>
      <div class="card-header">
        <h3>
          <el-icon><ChatDotRound /></el-icon> 思辨剧场 - 互动推荐
        </h3>
        <el-button
          type="primary"
          plain
          @click="openTopicDialog"
          :loading="isLoadingInteractions"
          icon="Pointer"
          size="small"
        >
          {{ isLoadingInteractions ? '正在获取...' : '获取互动推荐' }}
        </el-button>
      </div>
    </template>

    <!-- 主题输入对话框 -->
    <el-dialog v-model="showTopicDialog" title="输入主题" width="30%" :close-on-click-modal="false">
      <el-input
        v-model="topicInput"
        placeholder="请输入主题，如：光合作用"
        @keyup.enter="handleTopicConfirm"
      />
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showTopicDialog = false">取消</el-button>
          <el-button type="primary" @click="handleTopicConfirm"> 确认 </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- Loading State -->
    <div v-if="isLoadingInteractions" class="loading-placeholder">
      <el-skeleton :rows="3" animated />
    </div>

    <!-- Recommendation List -->
    <el-collapse v-else-if="recommendedInteractions.length > 0" accordion>
      <el-collapse-item v-for="(item, index) in recommendedInteractions" :key="index" :name="index">
        <template #title>
          <el-tag
            size="small"
            :type="
              item.type === '提问策略'
                ? 'primary'
                : item.type === '小组活动'
                  ? 'success'
                  : 'warning'
            "
            style="margin-right: 8px"
          >
            {{ item.type }}
          </el-tag>
          <span class="interaction-title">{{ item.title }}</span>
        </template>
        <div class="interaction-content" v-html="md.render(item.content.join('\n'))"></div>
      </el-collapse-item>
    </el-collapse>

    <!-- Empty State -->
    <el-empty v-else description="暂无推荐，请先输入主题获取推荐"></el-empty>
  </el-card>
</template>

<style scoped>
.interactions-card {
  margin-bottom: 30px;
}

.interactions-card .card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.interactions-card .card-header h3 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 5px;
}

.interaction-title {
  font-weight: 500;
}

.interaction-content {
  padding: 10px 40px;
  line-height: 1.7;
  background-color: #fafafa;
  border-radius: 4px;
}

.loading-placeholder {
  padding: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}
</style>
