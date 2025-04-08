<script setup lang="ts">
import { ref, reactive } from 'vue';
import { ElMessage } from 'element-plus';
import { ArrowUp, ArrowDown, Delete } from '@element-plus/icons-vue';
import type { Question } from '@/api';

interface PaperInfo {
  title: string;
  totalScore: number;
  duration: number;
  description: string;
}

const selectedQuestions = ref<Question[]>([]);
const paperInfo = reactive<PaperInfo>({
  title: '',
  totalScore: 100,
  duration: 120,
  description: '',
});

const defaultScores = {
  选择题: 5,
  填空题: 5,
  判断题: 3,
  简答题: 10,
};

// 计算试卷总分
const calculateTotalScore = (): number => {
  return selectedQuestions.value.reduce((total, q) => {
    return total + (defaultScores[q.type as keyof typeof defaultScores] || 0);
  }, 0);
};

// 移除试题
const removeQuestion = (index: number) => {
  selectedQuestions.value.splice(index, 1);
};

// 调整试题顺序
const moveQuestion = (index: number, direction: 'up' | 'down') => {
  if (direction === 'up' && index > 0) {
    [selectedQuestions.value[index], selectedQuestions.value[index - 1]] = [
      selectedQuestions.value[index - 1],
      selectedQuestions.value[index],
    ];
  } else if (direction === 'down' && index < selectedQuestions.value.length - 1) {
    [selectedQuestions.value[index], selectedQuestions.value[index + 1]] = [
      selectedQuestions.value[index + 1],
      selectedQuestions.value[index],
    ];
  }
};

// 导出试卷
const exportPaper = () => {
  if (!paperInfo.title) {
    ElMessage.warning('请填写试卷标题');
    return;
  }

  const paperData = {
    ...paperInfo,
    questions: selectedQuestions.value,
    totalScore: calculateTotalScore(),
  };

  // 创建并下载试卷文件
  const blob = new Blob([JSON.stringify(paperData, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `${paperInfo.title}.json`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);

  ElMessage.success('试卷导出成功');
};

// 导出为 Word 格式
const exportToWord = () => {
  // TODO: 实现 Word 格式导出
  ElMessage.info('Word格式导出功能即将上线');
};

defineExpose({
  selectedQuestions,
});
</script>

<template>
  <div class="paper-preview">
    <!-- 试卷基本信息 -->
    <el-form :model="paperInfo" label-width="100px" class="paper-info">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="试卷标题" required>
            <el-input v-model="paperInfo.title" placeholder="请输入试卷标题"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="考试时长">
            <el-input-number
              v-model="paperInfo.duration"
              :min="30"
              :step="30"
              placeholder="分钟"
            ></el-input-number>
          </el-form-item>
        </el-col>
      </el-row>
      <el-form-item label="试卷说明">
        <el-input
          v-model="paperInfo.description"
          type="textarea"
          placeholder="请输入试卷说明"
          :rows="2"
        ></el-input>
      </el-form-item>
    </el-form>

    <!-- 已选题目列表 -->
    <div class="selected-questions">
      <div class="questions-header">
        <h4>已选题目</h4>
        <span class="total-score">总分：{{ calculateTotalScore() }}分</span>
      </div>

      <el-empty v-if="selectedQuestions.length === 0" description="暂无已选题目"></el-empty>
      <el-table v-else :data="selectedQuestions" style="width: 100%" max-height="400">
        <el-table-column type="index" width="50" label="序号"></el-table-column>
        <el-table-column prop="type" label="题型" width="100"></el-table-column>
        <el-table-column prop="stem" label="题干" show-overflow-tooltip></el-table-column>
        <el-table-column label="分值" width="80">
          <template #default="scope">
            {{ defaultScores[scope.row.type as keyof typeof defaultScores] }}分
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button-group>
              <el-button
                type="primary"
                :icon="ArrowUp"
                link
                @click="moveQuestion(scope.$index, 'up')"
                :disabled="scope.$index === 0"
              ></el-button>
              <el-button
                type="primary"
                :icon="ArrowDown"
                link
                @click="moveQuestion(scope.$index, 'down')"
                :disabled="scope.$index === selectedQuestions.length - 1"
              ></el-button>
              <el-button
                type="danger"
                :icon="Delete"
                link
                @click="removeQuestion(scope.$index)"
              ></el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 导出按钮 -->
    <div class="export-buttons">
      <el-button-group>
        <el-button type="primary" @click="exportPaper" :disabled="selectedQuestions.length === 0">
          导出试卷
        </el-button>
        <el-button type="success" @click="exportToWord" :disabled="selectedQuestions.length === 0">
          导出Word
        </el-button>
      </el-button-group>
    </div>
  </div>
</template>

<style scoped>
.paper-preview {
  padding: 0 20px;
}

.paper-info {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.selected-questions {
  margin: 20px 0;
}

.questions-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.questions-header h4 {
  margin: 0;
}

.total-score {
  font-size: 16px;
  color: #409eff;
  font-weight: bold;
}

.export-buttons {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  padding-top: 20px;
  border-top: 1px solid #eee;
}
</style>
