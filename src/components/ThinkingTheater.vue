<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { ElMessage } from 'element-plus'

// 互动环节数据结构
interface Interaction {
  id: number;
  type: string;
  title: string;
  content: string;
  tags: string[];
}

// 情景模拟数据结构
interface Scenario {
  id: number;
  title: string;
  description: string;
  background: string;
  objectives: string[];
  difficulty: string;
}

// 互动环节列表
const interactions = ref<Interaction[]>([
  {
    id: 1,
    type: '提问策略',
    title: '苏格拉底式提问法',
    content: '通过一系列引导性问题，帮助学生自己发现知识点和解决问题的方法。\n1. 你认为...的核心概念是什么？请用自己的话解释。\n2. 这个概念与我们之前学过的...有什么联系？\n3. 如果改变...中的某个条件，可能会产生什么不同的结果？',
    tags: ['批判性思维', '高阶思维', '通用']
  },
  {
    id: 2,
    type: '小组活动',
    title: '思维导图协作',
    content: '将学生分成4-5人小组，每组使用一张大纸，围绕中心概念创建思维导图，展示概念间的联系。\n- 第一阶段(10分钟)：每人负责一个分支\n- 第二阶段(5分钟)：小组讨论并连接不同分支\n- 第三阶段(5分钟)：小组展示',
    tags: ['合作学习', '可视化', '知识整合']
  },
  {
    id: 3,
    type: '思辨讨论',
    title: '六顶思考帽',
    content: '使用六顶思考帽方法进行多角度思考：\n- 白帽：关注客观事实和数据\n- 红帽：表达情感和直觉反应\n- 黑帽：指出风险和问题\n- 黄帽：寻找优点和价值\n- 绿帽：提出创新和替代方案\n- 蓝帽：负责总结和流程控制',
    tags: ['多角度思考', '结构化讨论', '高中适用']
  },
  {
    id: 4,
    type: '角色扮演',
    title: '历史人物对话',
    content: '学生扮演不同历史时期或不同立场的人物，围绕特定话题进行对话或辩论。\n准备阶段：\n- 研究人物背景和观点\n- 准备符合人物身份的论点\n表演阶段：\n- 按照时间线或议题展开对话\n- 其他学生可提问或评论',
    tags: ['历史', '语文', '跨学科']
  }
]);

// 情景模拟沙盘列表
const scenarios = ref<Scenario[]>([
  {
    id: 1,
    title: '古诗创作场景',
    description: '模拟古代文人雅集场景，引导学生体验古诗创作过程',
    background: '你身处盛唐长安，正值春日，与友人在城外踏青赏花。看着眼前的美景，你准备即兴创作一首七言绝句...',
    objectives: ['理解古诗创作背景', '掌握七言绝句格律', '培养文学鉴赏能力'],
    difficulty: '中等'
  },
  {
    id: 2,
    title: '科学探究实验室',
    description: '模拟科学家进行实验探究的过程，培养科学思维和方法',
    background: '你是一位年轻的科学家，正在研究植物生长与环境因素的关系。你需要设计一个实验，控制变量并收集数据...',
    objectives: ['学习科学实验设计', '理解变量控制原理', '培养数据分析能力'],
    difficulty: '较难'
  },
  {
    id: 3,
    title: '历史决策模拟',
    description: '置身历史关键时刻，模拟历史人物面临的决策困境',
    background: '公元1839年，你是清朝钦差大臣林则徐，奉命到广州查禁鸦片。面对外国商人的抵制和朝廷的压力，你需要决定如何处理查获的鸦片...',
    objectives: ['理解历史背景与影响因素', '培养多角度分析能力', '锻炼决策思维'],
    difficulty: '较难'
  },
  {
    id: 4,
    title: '数学应用情境',
    description: '将抽象数学概念应用到实际生活情境中',
    background: '你是一名建筑师，正在设计一座新的城市广场。你需要运用几何知识设计出美观且实用的空间布局...',
    objectives: ['理解数学在实际中的应用', '培养空间思维能力', '锻炼问题解决能力'],
    difficulty: '中等'
  }
]);

// 当前选中的互动或情景
const currentInteraction = ref<Interaction | null>(null);
const currentScenario = ref<Scenario | null>(null);

// 对话框控制
const showInteractionDialog = ref(false);
const showScenarioDialog = ref(false);

// 筛选条件
const interactionFilters = reactive({
  type: '',
  tag: ''
});

// 互动类型和标签选项
const interactionTypes = ['提问策略', '小组活动', '思辨讨论', '角色扮演'];
const interactionTags = ['批判性思维', '合作学习', '高阶思维', '多角度思考', '跨学科'];

// 筛选互动环节
const filteredInteractions = computed(() => {
  return interactions.value.filter(item => {
    if (interactionFilters.type && item.type !== interactionFilters.type) return false;
    if (interactionFilters.tag && !item.tags.includes(interactionFilters.tag)) return false;
    return true;
  });
});

// 打开互动详情
const openInteractionDetail = (interaction: Interaction) => {
  currentInteraction.value = interaction;
  showInteractionDialog.value = true;
};

// 打开情景模拟
const openScenarioDetail = (scenario: Scenario) => {
  currentScenario.value = scenario;
  showScenarioDialog.value = true;
};

// 创建新互动环节（占位函数）
const createNewInteraction = () => {
  ElMessage.info('创建新互动环节功能即将上线');
};

// 创建新情景模拟（占位函数）
const createNewScenario = () => {
  ElMessage.info('创建新情景模拟功能即将上线');
};

// 模拟提交互动结果
const submitInteractionResult = () => {
  ElMessage.success('互动结果已保存');
  showInteractionDialog.value = false;
};

// 模拟提交情景模拟结果
const submitScenarioResult = () => {
  ElMessage.success('模拟结果已保存');
  showScenarioDialog.value = false;
};
</script>

<template>
  <div class="thinking-theater-container">
    <div class="theater-header">
      <h2 class="section-title">思辨剧场</h2>
      <div class="header-actions">
        <el-button type="primary" @click="createNewInteraction" icon="Plus">创建互动环节</el-button>
        <el-button type="warning" @click="createNewScenario" icon="VideoPlay">创建情景模拟</el-button>
      </div>
    </div>

    <!-- 互动环节区域 -->
    <el-card class="theater-card">
      <template #header>
        <div class="card-header">
          <h3><el-icon>
              <ChatDotRound />
            </el-icon> 互动环节推荐</h3>
          <div class="filter-actions">
            <el-select v-model="interactionFilters.type" placeholder="互动类型" clearable size="small">
              <el-option v-for="type in interactionTypes" :key="type" :label="type" :value="type"></el-option>
            </el-select>
            <el-select v-model="interactionFilters.tag" placeholder="标签筛选" clearable size="small">
              <el-option v-for="tag in interactionTags" :key="tag" :label="tag" :value="tag"></el-option>
            </el-select>
          </div>
        </div>
      </template>

      <div class="interaction-list">
        <el-card v-for="item in filteredInteractions" :key="item.id" class="interaction-item" shadow="hover"
          @click="openInteractionDetail(item)">
          <div class="interaction-item-header">
            <el-tag
              :type="item.type === '提问策略' ? 'primary' : (item.type === '小组活动' ? 'success' : (item.type === '思辨讨论' ? 'warning' : 'info'))">
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
          <h3><el-icon>
              <VideoPlay />
            </el-icon> 情景模拟沙盘</h3>
        </div>
      </template>

      <div class="scenario-list">
        <el-card v-for="item in scenarios" :key="item.id" class="scenario-item" shadow="hover"
          @click="openScenarioDetail(item)">
          <div class="scenario-item-header">
            <h4>{{ item.title }}</h4>
            <el-tag :type="item.difficulty === '简单' ? 'success' : (item.difficulty === '中等' ? 'warning' : 'danger')"
              size="small">
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
    <el-dialog v-model="showInteractionDialog" :title="currentInteraction?.title || '互动环节详情'" width="60%">
      <div v-if="currentInteraction" class="interaction-detail">
        <div class="detail-header">
          <el-tag
            :type="currentInteraction.type === '提问策略' ? 'primary' : (currentInteraction.type === '小组活动' ? 'success' : (currentInteraction.type === '思辨讨论' ? 'warning' : 'info'))">
            {{ currentInteraction.type }}
          </el-tag>
          <div class="detail-tags">
            <el-tag v-for="(tag, index) in currentInteraction.tags" :key="index" size="small" effect="plain">
              {{ tag }}
            </el-tag>
          </div>
        </div>

        <div class="detail-content" v-html="currentInteraction.content.replace(/\n/g, '<br/>')"></div>

        <div class="detail-actions">
          <h4>应用到课堂</h4>
          <el-form label-position="top">
            <el-form-item label="适用课题">
              <el-input placeholder="输入适用的课题名称"></el-input>
            </el-form-item>
            <el-form-item label="预计时间">
              <el-input-number :min="5" :max="45" :step="5" placeholder="分钟"></el-input-number>
            </el-form-item>
            <el-form-item label="教学笔记">
              <el-input type="textarea" :rows="3" placeholder="记录如何将此互动应用到您的课堂..."></el-input>
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
    <el-dialog v-model="showScenarioDialog" :title="currentScenario?.title || '情景模拟'" width="70%">
      <div v-if="currentScenario" class="scenario-detail">
        <div class="detail-header">
          <el-tag
            :type="currentScenario.difficulty === '简单' ? 'success' : (currentScenario.difficulty === '中等' ? 'warning' : 'danger')">
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
          <el-input type="textarea" :rows="5" placeholder="在此处输入您的模拟操作或回应..."></el-input>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showScenarioDialog = false">关闭</el-button>
          <el-button type="primary" @click="submitScenarioResult">提交模拟</el-button>
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