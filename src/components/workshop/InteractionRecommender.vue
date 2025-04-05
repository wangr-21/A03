<script setup lang="ts">
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import MarkdownIt from 'markdown-it';
import { getRecommendedInteractions } from '@/api';
import type { InteractionItem } from '@/api';

const md = new MarkdownIt();

// Ref for recommended interactions
const recommendedInteractions = ref<InteractionItem[]>([]);
const isLoadingInteractions = ref<boolean>(false);

// Function to fetch recommended interactions
const fetchRecommendedInteractions = async (topic: string = '{topic}'): Promise<void> => {
  isLoadingInteractions.value = true;
  recommendedInteractions.value = []; // Clear previous recommendations
  console.log('Fetching recommended interactions based on:', topic);

  try {
    const response = await getRecommendedInteractions(topic);

    if (response.success) {
      recommendedInteractions.value = response.data;
      ElMessage.success('互动推荐获取成功！');
    } else {
      throw new Error('Interaction recommendation failed');
    }
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
    <template #header>
      <div class="card-header">
        <h3>
          <el-icon><ChatDotRound /></el-icon> 思辨剧场 - 互动推荐
        </h3>
        <el-button
          type="primary"
          plain
          @click="fetchRecommendedInteractions()"
          :loading="isLoadingInteractions"
          icon="Pointer"
          size="small"
        >
          {{ isLoadingInteractions ? '正在获取...' : '获取互动推荐' }}
        </el-button>
      </div>
    </template>

    <!-- Loading State -->
    <div v-if="isLoadingInteractions" class="loading-placeholder">
      <el-skeleton :rows="3" animated />
    </div>

    <!-- Recommendation List (using el-collapse) -->
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
        <div class="interaction-content" v-html="md.render(item.content)"></div>
      </el-collapse-item>
    </el-collapse>

    <!-- Empty State -->
    <el-empty v-else description="暂无推荐，请先点击按钮获取推荐"></el-empty>
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
  padding: 10px 15px;
  line-height: 1.7;
  background-color: #fafafa;
  border-radius: 4px;
  white-space: pre-wrap; /* Preserve line breaks */
}

.loading-placeholder {
  padding: 20px;
}
</style>
