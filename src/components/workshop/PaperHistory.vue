<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { Refresh } from '@element-plus/icons-vue';
import type { Question } from '@/api';

interface HistoryPaper {
  id: string;
  title: string;
  createTime: string;
  totalScore: number;
  questionCount: number;
  questions: Question[];
}

const historyPapers = ref<HistoryPaper[]>([]);
const isLoading = ref(false);

// 模拟获取历史试卷数据
const fetchHistoryPapers = async () => {
  isLoading.value = true;
  try {
    // TODO: 替换为实际的API调用
    await new Promise(resolve => setTimeout(resolve, 500));
    historyPapers.value = [
      {
        id: '1',
        title: '2024年春季数学测试卷',
        createTime: '2024-03-20 14:30',
        totalScore: 100,
        questionCount: 20,
        questions: []
      },
      {
        id: '2',
        title: '2024年寒假作业试卷',
        createTime: '2024-01-15 09:45',
        totalScore: 120,
        questionCount: 25,
        questions: []
      }
    ];
  } catch (error) {
    console.error('获取历史试卷失败:', error);
    ElMessage.error('获取历史试卷失败');
  } finally {
    isLoading.value = false;
  }
};

// 查看历史试卷详情
// eslint-disable-next-line @typescript-eslint/no-unused-vars
const viewPaperDetail = (paper: HistoryPaper) => {
  // TODO: 实现查看详情逻辑
  ElMessage.info('查看试卷详情功能开发中');
};

// 复用历史试卷
// eslint-disable-next-line @typescript-eslint/no-unused-vars
const reusePaper = (paper: HistoryPaper) => {
  // TODO: 实现复用逻辑
  ElMessage.success('试卷复用功能开发中');
};

onMounted(() => {
  fetchHistoryPapers();
});
</script>

<template>
  <div class="paper-history">
    <div class="history-header">
      <h4>历史试卷记录</h4>
      <el-button type="primary" link @click="fetchHistoryPapers">
        <el-icon><Refresh /></el-icon>
        刷新
      </el-button>
    </div>

    <div class="history-list" v-loading="isLoading">
      <el-empty v-if="historyPapers.length === 0" description="暂无历史记录"></el-empty>
      <el-card
        v-else
        v-for="paper in historyPapers"
        :key="paper.id"
        class="history-item"
        shadow="hover"
      >
        <div class="paper-info">
          <h5 class="paper-title">{{ paper.title }}</h5>
          <div class="paper-meta">
            <span>创建时间：{{ paper.createTime }}</span>
            <span>总分：{{ paper.totalScore }}分</span>
            <span>题目数：{{ paper.questionCount }}</span>
          </div>
        </div>
        <div class="paper-actions">
          <el-button type="primary" link @click="viewPaperDetail(paper)">
            查看详情
          </el-button>
          <el-button type="success" link @click="reusePaper(paper)">
            复用试卷
          </el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<style scoped>
.paper-history {
  padding: 0 20px;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.history-header h4 {
  margin: 0;
}

.history-list {
  min-height: 200px;
}

.history-item {
  margin-bottom: 15px;
}

.history-item:last-child {
  margin-bottom: 0;
}

.paper-info {
  flex: 1;
}

.paper-title {
  margin: 0 0 10px 0;
  color: #303133;
}

.paper-meta {
  display: flex;
  gap: 20px;
  color: #909399;
  font-size: 14px;
}

.paper-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
  gap: 15px;
}
</style>
