<script setup lang="ts">
import { ref, reactive, PropType } from 'vue';
import { ElMessage } from 'element-plus';
import { Check, Microphone, Close, Loading } from '@element-plus/icons-vue';
import { getQuestions } from '@/api';
import type { Question } from '@/api';

// 声明props，接收PaperPreview组件引用以便添加生成的题目
const props = defineProps({
  paperPreviewRef: {
    type: Object as PropType<{ selectedQuestions: Question[] }>,
    required: true,
  },
});

// 声明emit，用于关闭对话框
const emit = defineEmits(['close']);

// 生成器设置
const generatorSettings = reactive({
  subject: '美术', // 默认学科为美术
  grade: '初中', // 年级
  difficulty: '', // 难度
  totalQuestions: 10, // 总题数
  questionTypes: [] as string[], // 题型分布
  knowledgePoints: [] as string[], // 知识点
  description: '', // 自然语言描述
  isGenerating: false, // 是否正在生成
  success: false, // 是否生成成功
});

// 学科选项（美术及相关学科）
const subjectOptions = [
  '美术',
  '美术鉴赏',
  '设计与工艺',
  '中国画',
  '书法',
  '水彩画',
  '素描',
  '综合材料',
];

// 年级选项
const gradeOptions = ['小学低年级', '小学中年级', '小学高年级', '初中'];

// 难度选项
const difficultyOptions = [
  { label: '基础', value: 'easy' },
  { label: '提高', value: 'medium' },
  { label: '拓展', value: 'hard' },
];

// 题型选项（美术学科特有题型）
const questionTypeOptions = ['鉴赏题', '创作表现题', '技法应用题', '材料工具题', '美术史论题', '综合探究题'];

// 知识点选项 (会根据学科动态变化)
const knowledgePointOptions = ref([
  '色彩理论',
  '构图基础',
  '透视原理',
  '中国画技法',
  '西方绘画史',
  '中国美术史',
  '设计元素',
  '民间美术',
  '现代艺术',
]);

// 根据所选学科更新知识点选项
const updateKnowledgePoints = () => {
  // 根据不同学科设置不同的知识点选项
  switch (generatorSettings.subject) {
    case '美术':
      knowledgePointOptions.value = ['色彩理论', '构图基础', '透视原理', '中国美术史', '西方美术史', '创意思维'];
      break;
    case '美术鉴赏':
      knowledgePointOptions.value = ['艺术风格', '作品分析', '艺术流派', '中国传统绘画', '西方经典绘画', '现当代艺术'];
      break;
    case '设计与工艺':
      knowledgePointOptions.value = ['平面设计', '立体构成', '工艺材料', '民间工艺', '设计原理', '创新设计'];
      break;
    case '中国画':
      knowledgePointOptions.value = ['山水画', '花鸟画', '人物画', '写意技法', '工笔技法', '传统颜料'];
      break;
    case '书法':
      knowledgePointOptions.value = ['楷书', '行书', '草书', '篆书', '隶书', '书法史', '书法欣赏'];
      break;
    case '水彩画':
      knowledgePointOptions.value = ['湿画法', '干画法', '水彩技巧', '水彩风景', '水彩静物', '混合技法'];
      break;
    case '素描':
      knowledgePointOptions.value = ['素描基础', '明暗关系', '结构素描', '石膏几何体', '静物素描', '人物素描'];
      break;
    case '综合材料':
      knowledgePointOptions.value = ['纸艺', '版画', '陶艺', '雕塑', '装置艺术', '数字媒体'];
      break;
    default:
      knowledgePointOptions.value = ['基础理论', '技法应用', '艺术欣赏', '创意表达', '美术史', '传统文化'];
      break;
  }
  // 重置已选知识点，避免出现不合理的选择
  generatorSettings.knowledgePoints = [];
};

// 模拟AI生成试卷
const generateAIPaper = async () => {
  // 验证表单
  if (!generatorSettings.subject) {
    ElMessage.warning('请选择学科');
    return;
  }

  // 如果没有描述，至少要有一些基本设置
  if (!generatorSettings.description && (!generatorSettings.questionTypes.length || !generatorSettings.knowledgePoints.length)) {
    ElMessage.warning('请提供试卷描述或者设置题型和知识点');
    return;
  }

  try {
    generatorSettings.isGenerating = true;
    generatorSettings.success = false;

    // 模拟API请求延迟
    await new Promise((resolve) => setTimeout(resolve, 2000));

    // 构建查询参数
    const filters = {
      type: generatorSettings.questionTypes.length ? generatorSettings.questionTypes : undefined,
      difficulty: generatorSettings.difficulty || undefined,
      knowledgePoint: generatorSettings.knowledgePoints.length ? generatorSettings.knowledgePoints[0] : undefined,
      subject: generatorSettings.subject,
      page: 1,
      pageSize: 50,
    };

    // 获取题目
    const response = await getQuestions(filters);

    if (response.success && response.data.questions.length > 0) {
      // 排序和筛选题目，模拟AI的智能选择
      const questions = response.data.questions;
      
      // 模拟AI根据描述进行题目选择
      let selectedQuestions = [...questions];
      
      // 根据总题目数进行限制
      const numToSelect = Math.min(generatorSettings.totalQuestions, selectedQuestions.length);
      selectedQuestions = selectedQuestions.slice(0, numToSelect);
      
      // 添加到paperPreviewRef
      if (props.paperPreviewRef) {
        // 清除之前的选择
        props.paperPreviewRef.selectedQuestions.length = 0;
        
        // 添加新选择的题目
        selectedQuestions.forEach(q => {
          props.paperPreviewRef.selectedQuestions.push(q);
        });
        
        generatorSettings.success = true;
        ElMessage.success(`已成功生成${selectedQuestions.length}道美术试题`);
      }
    } else {
      ElMessage.warning('没有找到符合条件的题目，请调整筛选条件');
    }
  } catch (error) {
    console.error('生成试卷时出错:', error);
    ElMessage.error('生成试卷失败，请稍后重试');
  } finally {
    generatorSettings.isGenerating = false;
  }
};

// 完成试卷生成，关闭对话框
const finishGeneration = () => {
  emit('close');
};
</script>

<template>
  <div class="ai-paper-generator">
    <div v-if="generatorSettings.success" class="success-panel">
      <div class="success-icon">
        <el-icon><Check /></el-icon>
      </div>
      <h2>美术试卷生成成功！</h2>
      <p>已将生成的题目添加到试卷中，您可以在"试卷生成"面板中查看和编辑。</p>
      <el-button type="primary" @click="finishGeneration">完成</el-button>
    </div>
    
    <div v-else class="generator-form">
      <div class="form-header">
        <h4>通过AI智能生成美术学科试卷</h4>
        <p class="form-tip">您可以通过自然语言描述需求，或使用下方表单进行精确设置</p>
      </div>
      
      <el-form :model="generatorSettings" label-position="top">
        <!-- 自然语言描述 -->
        <el-form-item label="试卷需求描述">
          <el-input
            v-model="generatorSettings.description"
            type="textarea"
            :rows="3"
            placeholder="请描述您需要的美术试卷，例如：'我需要一份初中美术色彩理论的练习题，包含基础和提高难度的题目，主要考察色彩基本原理和配色技巧'"
          ></el-input>
        </el-form-item>
        
        <div class="form-divider">
          <span>或者精确设置</span>
        </div>
        
        <!-- 基础设置 -->
        <div class="form-row">
          <el-form-item label="学科">
            <el-select 
              v-model="generatorSettings.subject" 
              placeholder="选择美术相关学科"
              @change="updateKnowledgePoints"
            >
              <el-option
                v-for="item in subjectOptions"
                :key="item"
                :label="item"
                :value="item"
              ></el-option>
            </el-select>
          </el-form-item>
          
          <el-form-item label="年级">
            <el-select v-model="generatorSettings.grade" placeholder="选择年级">
              <el-option
                v-for="item in gradeOptions"
                :key="item"
                :label="item"
                :value="item"
              ></el-option>
            </el-select>
          </el-form-item>
          
          <el-form-item label="难度">
            <el-select v-model="generatorSettings.difficulty" placeholder="选择难度" clearable>
              <el-option
                v-for="item in difficultyOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              ></el-option>
            </el-select>
          </el-form-item>
        </div>
        
        <div class="form-row">
          <el-form-item label="总题数">
            <el-input-number v-model="generatorSettings.totalQuestions" :min="1" :max="30"></el-input-number>
          </el-form-item>
        </div>
        
        <!-- 题型设置 -->
        <el-form-item label="题型分布">
          <el-checkbox-group v-model="generatorSettings.questionTypes">
            <el-checkbox 
              v-for="type in questionTypeOptions" 
              :key="type" 
              :label="type"
            >
              {{ type }}
            </el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        
        <!-- 知识点设置 -->
        <el-form-item label="知识点">
          <el-select
            v-model="generatorSettings.knowledgePoints"
            multiple
            collapse-tags
            placeholder="选择知识点"
            style="width: 100%"
          >
            <el-option
              v-for="item in knowledgePointOptions"
              :key="item"
              :label="item"
              :value="item"
            ></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      
      <!-- 生成按钮 -->
      <div class="form-actions">
        <el-button @click="emit('close')">取消</el-button>
        <el-button 
          type="primary" 
          @click="generateAIPaper" 
          :loading="generatorSettings.isGenerating"
          :disabled="generatorSettings.isGenerating"
        >
          <el-icon v-if="!generatorSettings.isGenerating"><Microphone /></el-icon>
          <span>{{ generatorSettings.isGenerating ? '正在生成中...' : '智能生成美术试卷' }}</span>
        </el-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ai-paper-generator {
  padding: 0 20px;
}

.generator-form {
  padding: 0;
}

.form-header {
  margin-bottom: 24px;
  text-align: center;
}

.form-header h4 {
  font-size: 18px;
  font-weight: 500;
  color: var(--el-text-color-primary);
  margin: 0 0 8px 0;
}

.form-tip {
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin: 0;
}

.form-divider {
  display: flex;
  align-items: center;
  margin: 20px 0;
  color: var(--el-text-color-secondary);
  font-size: 14px;
}

.form-divider::before,
.form-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background-color: var(--el-border-color-lighter);
}

.form-divider span {
  padding: 0 10px;
}

.form-row {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.form-row .el-form-item {
  flex: 1;
  margin-bottom: 0;
}

.form-actions {
  display: flex;
  justify-content: center;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid var(--el-border-color-lighter);
  gap: 16px;
}

.success-panel {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  text-align: center;
}

.success-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: var(--el-color-success-light);
  color: var(--el-color-success);
  margin-bottom: 24px;
}

.success-icon .el-icon {
  font-size: 40px;
}

.success-panel h2 {
  margin: 0 0 16px 0;
  font-size: 24px;
  color: var(--el-text-color-primary);
}

.success-panel p {
  margin: 0 0 32px 0;
  color: var(--el-text-color-secondary);
  font-size: 16px;
  max-width: 400px;
}
</style> 