<script setup lang="ts">
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { ElMessage } from 'element-plus';
import {
  getInteractions,
  getScenarios,
  // createInteraction,
  // createScenario,
  saveInteractionNote,
  submitScenarioResult,
} from '@/api/thinking';
import type {
  Interaction,
  Scenario,
  InteractionFilters,
  InteractionNote,
} from '@/api/thinking';

// 互动环节列表
const interactions = ref<Interaction[]>([]);
const scenarios = ref<Scenario[]>([]);

// 当前选中的互动或情景
const currentInteraction = ref<Interaction | null>(null);
const currentScenario = ref<Scenario | null>(null);

// 对话框控制
const showInteractionDialog = ref(false);
const showScenarioDialog = ref(false);
const isLoading = ref(false);

// 应用笔记
const interactionNote = reactive<InteractionNote>({
  topic: '',
  duration: 15,
  notes: '',
  interactionId: 0,
});

// 情景模拟响应
const scenarioResponse = ref('');

// 筛选条件
const interactionFilters = reactive<InteractionFilters>({
  type: '',
  tag: '',
});

// 互动类型和标签选项
const interactionTypes = ['提问策略', '小组活动', '思辨讨论', '角色扮演'];
const interactionTags = ['批判性思维', '合作学习', '高阶思维', '多角度思考', '跨学科'];

// 筛选互动环节
const filteredInteractions = computed(() => {
  return interactions.value;
});

// 加载互动环节数据
const loadInteractions = async () => {
  isLoading.value = true;
  try {
    interactions.value = await getInteractions(interactionFilters);
  } catch (error) {
    console.error('Failed to load interactions:', error);
    ElMessage.error('加载互动环节数据失败');
  } finally {
    isLoading.value = false;
  }
};

// 加载情景模拟数据
const loadScenarios = async () => {
  isLoading.value = true;
  try {
    scenarios.value = await getScenarios();
  } catch (error) {
    console.error('Failed to load scenarios:', error);
    ElMessage.error('加载情景模拟数据失败');
  } finally {
    isLoading.value = false;
  }
};

// 监听筛选条件变化
watch(interactionFilters, () => {
  loadInteractions();
});

// 打开互动详情
const openInteractionDetail = (interaction: Interaction) => {
  currentInteraction.value = interaction;
  // 重置应用笔记
  interactionNote.topic = '';
  interactionNote.duration = 15;
  interactionNote.notes = '';
  showInteractionDialog.value = true;
};

// 打开情景模拟
const openScenarioDetail = (scenario: Scenario) => {
  currentScenario.value = scenario;
  scenarioResponse.value = '';
  showScenarioDialog.value = true;
};

// 创建新互动环节
const createNewInteraction = async () => {
  ElMessage.info('创建新互动环节功能即将上线');
  // 实际实现时可以打开一个表单对话框，收集数据后调用createInteraction API
  // createInteraction
};

// 创建新情景模拟
const createNewScenario = async () => {
  ElMessage.info('创建新情景模拟功能即将上线');
  // 实际实现时可以打开一个表单对话框，收集数据后调用createScenario API
  // createScenario
};

// 提交互动结果
const submitInteractionResult = async () => {
  if (!currentInteraction.value) return;

  if (!interactionNote.topic) {
    ElMessage.warning('请输入适用课题');
    return;
  }

  try {
    const result = await saveInteractionNote({
      interactionId: currentInteraction.value.id,
      topic: interactionNote.topic,
      duration: interactionNote.duration,
      notes: interactionNote.notes,
    });

    if (result.success) {
      ElMessage.success('互动应用已保存');
      showInteractionDialog.value = false;
    } else {
      throw new Error('Failed to save');
    }
  } catch (error) {
    console.error('Error saving interaction note:', error);
    ElMessage.error('保存失败，请重试');
  }
};

// 提交情景模拟结果
const submitScenarioResultFunc = async () => {
  if (!currentScenario.value) return;

  if (!scenarioResponse.value.trim()) {
    ElMessage.warning('请输入您的模拟响应');
    return;
  }

  try {
    const result = await submitScenarioResult({
      scenarioId: currentScenario.value.id,
      response: scenarioResponse.value,
    });

    if (result.success) {
      ElMessage.success('模拟结果已保存');
      showScenarioDialog.value = false;
    } else {
      throw new Error('Failed to submit');
    }
  } catch (error) {
    console.error('Error submitting scenario result:', error);
    ElMessage.error('提交失败，请重试');
  }
};

// 组件挂载时加载数据
onMounted(() => {
  loadInteractions();
  loadScenarios();
});
</script>

<template>
  <div class="thinking-theater-container">
    <div class="theater-header">
      <h2 class="section-title">思辨剧场</h2>
      <div class="header-actions">
        <el-button type="primary" @click="createNewInteraction" icon="Plus">创建互动环节</el-button>
        <el-button type="warning" @click="createNewScenario" icon="VideoPlay"
          >创建情景模拟</el-button
        >
      </div>
    </div>

    <!-- 互动环节区域 -->
    <el-card class="theater-card">
      <template #header>
        <div class="card-header">
          <h3>
            <el-icon>
              <ChatDotRound />
            </el-icon>
            互动环节推荐
          </h3>
          <div class="filter-actions">
            <el-select
              v-model="interactionFilters.type"
              placeholder="互动类型"
              clearable
              size="small"
            >
              <el-option
                v-for="type in interactionTypes"
                :key="type"
                :label="type"
                :value="type"
              ></el-option>
            </el-select>
            <el-select
              v-model="interactionFilters.tag"
              placeholder="标签筛选"
              clearable
              size="small"
            >
              <el-option
                v-for="tag in interactionTags"
                :key="tag"
                :label="tag"
                :value="tag"
              ></el-option>
            </el-select>
          </div>
        </div>
      </template>

      <div class="interaction-list">
        <el-card
          v-for="item in filteredInteractions"
          :key="item.id"
          class="interaction-item"
          shadow="hover"
          @click="openInteractionDetail(item)"
        >
          <div class="interaction-item-header">
            <el-tag
              :type="
                item.type === '提问策略'
                  ? 'primary'
                  : item.type === '小组活动'
                    ? 'success'
                    : item.type === '思辨讨论'
                      ? 'warning'
                      : 'info'
              "
            >
              {{ item.type }}
            </el-tag>
            <h4>{{ item.title }}</h4>
          </div>
          <p class="interaction-preview">{{ item.content.split('\n')[0] }}</p>
          <div class="interaction-tags">
            <el-tag v-for="(tag, index) in item.tags" :key="index" size="small" effect="plain">
              {{ tag }}
            </el-tag>
          </div>
        </el-card>
      </div>
    </el-card>

    <!-- 情景模拟沙盘区域 -->
    <el-card class="theater-card">
      <template #header>
        <div class="card-header">
          <h3>
            <el-icon>
              <VideoPlay />
            </el-icon>
            情景模拟沙盘
          </h3>
        </div>
      </template>

      <div class="scenario-list">
        <el-card
          v-for="item in scenarios"
          :key="item.id"
          class="scenario-item"
          shadow="hover"
          @click="openScenarioDetail(item)"
        >
          <div class="scenario-item-header">
            <h4>{{ item.title }}</h4>
            <el-tag
              :type="
                item.difficulty === '简单'
                  ? 'success'
                  : item.difficulty === '中等'
                    ? 'warning'
                    : 'danger'
              "
              size="small"
            >
              {{ item.difficulty }}
            </el-tag>
          </div>
          <p class="scenario-description">{{ item.description }}</p>
          <div class="scenario-objectives">
            <span class="objective-label">教学目标：</span>
            <span>{{ item.objectives[0] }}</span>
          </div>
        </el-card>
      </div>
    </el-card>

    <!-- 互动环节详情对话框 -->
    <el-dialog
      v-model="showInteractionDialog"
      :title="currentInteraction?.title || '互动环节详情'"
      width="60%"
    >
      <div v-if="currentInteraction" class="interaction-detail">
        <div class="detail-header">
          <el-tag
            :type="
              currentInteraction.type === '提问策略'
                ? 'primary'
                : currentInteraction.type === '小组活动'
                  ? 'success'
                  : currentInteraction.type === '思辨讨论'
                    ? 'warning'
                    : 'info'
            "
          >
            {{ currentInteraction.type }}
          </el-tag>
          <div class="detail-tags">
            <el-tag
              v-for="(tag, index) in currentInteraction.tags"
              :key="index"
              size="small"
              effect="plain"
            >
              {{ tag }}
            </el-tag>
          </div>
        </div>

        <div
          class="detail-content"
          v-html="currentInteraction.content.replace(/\n/g, '<br/>')"
        ></div>

        <div class="detail-actions">
          <h4>应用到课堂</h4>
          <el-form label-position="top">
            <el-form-item label="适用课题">
              <el-input v-model="interactionNote.topic" placeholder="输入适用的课题名称"></el-input>
            </el-form-item>
            <el-form-item label="预计时间">
              <el-input-number
                v-model="interactionNote.duration"
                :min="5"
                :max="45"
                :step="5"
                placeholder="分钟"
              >
              </el-input-number>
            </el-form-item>
            <el-form-item label="教学笔记">
              <el-input
                type="textarea"
                :rows="3"
                v-model="interactionNote.notes"
                placeholder="记录如何将此互动应用到您的课堂..."
              ></el-input>
            </el-form-item>
          </el-form>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showInteractionDialog = false">关闭</el-button>
          <el-button type="success" @click="submitInteractionResult">保存应用</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 情景模拟详情对话框 -->
    <el-dialog
      v-model="showScenarioDialog"
      :title="currentScenario?.title || '情景模拟'"
      width="70%"
    >
      <div v-if="currentScenario" class="scenario-detail">
        <div class="detail-header">
          <el-tag
            :type="
              currentScenario.difficulty === '简单'
                ? 'success'
                : currentScenario.difficulty === '中等'
                  ? 'warning'
                  : 'danger'
            "
          >
            难度：{{ currentScenario.difficulty }}
          </el-tag>
        </div>

        <div class="scenario-background">
          <h4>情景背景</h4>
          <p>{{ currentScenario.background }}</p>
        </div>

        <div class="scenario-objectives">
          <h4>教学目标</h4>
          <ul>
            <li v-for="(objective, index) in currentScenario.objectives" :key="index">
              {{ objective }}
            </li>
          </ul>
        </div>

        <div class="simulation-area">
          <h4>模拟操作</h4>
          <el-input
            type="textarea"
            :rows="5"
            v-model="scenarioResponse"
            placeholder="在此处输入您的模拟操作或回应..."
          ></el-input>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showScenarioDialog = false">关闭</el-button>
          <el-button type="primary" @click="submitScenarioResultFunc">提交模拟</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.thinking-theater-container {
  margin-bottom: 30px;
}

.theater-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  font-size: 22px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.theater-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 5px;
}

.filter-actions {
  display: flex;
  gap: 10px;
}

.interaction-list,
.scenario-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 15px;
  margin-top: 15px;
}

.interaction-item,
.scenario-item {
  cursor: pointer;
  transition: all 0.3s ease;
}

.interaction-item:hover,
.scenario-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.interaction-item-header,
.scenario-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.interaction-item-header h4,
.scenario-item-header h4 {
  margin: 0;
  font-size: 16px;
  font-weight: bold;
}

.interaction-preview,
.scenario-description {
  color: #666;
  margin-bottom: 10px;
  height: 40px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
}

.interaction-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.scenario-objectives {
  font-size: 13px;
  color: #666;
}

.objective-label {
  font-weight: bold;
}

/* 详情对话框样式 */
.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.detail-tags {
  display: flex;
  gap: 5px;
}

.detail-content {
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 20px;
  line-height: 1.6;
}

.detail-actions {
  border-top: 1px solid #eee;
  padding-top: 15px;
  margin-top: 15px;
}

.detail-actions h4 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
}

.scenario-background,
.scenario-objectives,
.simulation-area {
  margin-bottom: 20px;
}

.scenario-background h4,
.scenario-objectives h4,
.simulation-area h4 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #333;
}

.scenario-objectives ul {
  padding-left: 20px;
  margin: 0;
}

.scenario-objectives li {
  margin-bottom: 5px;
}
</style>
