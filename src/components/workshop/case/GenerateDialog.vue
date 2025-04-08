<script setup lang="ts">
import { computed, reactive } from 'vue';
import type {
  DynastyInfo,
  ThemeCategory,
  DisciplineCategory,
  GenerateStoryRequest,
  GenerateCaseRequest,
} from '@/api';

const props = defineProps<{
  type: 'story' | 'case';
  dynasties: DynastyInfo[];
  themes: ThemeCategory[];
  disciplines: DisciplineCategory[];
}>();

const visible = defineModel<boolean>('visible', {
  default: false,
});

const emit = defineEmits<{
  'update:visible': [value: boolean];
  generate: [type: 'story' | 'case', data: GenerateStoryRequest | GenerateCaseRequest];
}>();

const storyForm = reactive<GenerateStoryRequest>({
  dynasty: undefined,
  theme: '',
  keywords: [],
});

const caseForm = reactive<GenerateCaseRequest>({
  story_id: undefined,
  main_discipline: '',
  related_disciplines: [],
  suitable_grades: '',
});

const dialogTitle = computed(() => (props.type === 'story' ? '生成故事' : '生成案例'));

const handleCancel = () => {
  emit('update:visible', false);
};

const handleGenerate = () => {
  if (props.type === 'story') {
    emit('generate', 'story', { ...storyForm });
  } else {
    emit('generate', 'case', { ...caseForm });
  }
};
</script>

<template>
  <el-dialog
    v-model="visible"
    :title="dialogTitle"
    width="500px"
    @update:visible="$emit('update:visible', $event)"
  >
    <!-- 故事生成表单 -->
    <el-form v-if="type === 'story'" :model="storyForm" label-width="100px">
        <el-form-item label="朝代">
          <el-select v-model="storyForm.dynasty">
            <el-option
              v-for="dynasty in dynasties"
              :key="dynasty.name"
              :label="dynasty.name"
              :value="dynasty.name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="主题">
          <el-select v-model="storyForm.theme">
            <el-option
              v-for="theme in themes"
              :key="theme.name"
              :label="theme.name"
              :value="theme.name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="关键词">
          <el-select v-model="storyForm.keywords" multiple>
            <template v-for="theme in themes" :key="theme.name">
              <el-option
                v-for="subcat in theme.subcategories"
                :key="`${theme.name}-${subcat}`"
                :label="subcat"
                :value="subcat"
              />
            </template>
          </el-select>
        </el-form-item>
    </el-form>

    <!-- 案例生成表单 -->
    <el-form v-else :model="caseForm" label-width="100px">
        <el-form-item label="主要学科">
          <el-select v-model="caseForm.main_discipline">
            <el-option
              v-for="discipline in disciplines"
              :key="discipline.name"
              :label="discipline.name"
              :value="discipline.name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="相关学科">
          <el-select v-model="caseForm.related_disciplines" multiple>
            <el-option
              v-for="discipline in disciplines"
              :key="discipline.name"
              :label="discipline.name"
              :value="discipline.name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="适用年级">
          <el-input v-model="caseForm.suitable_grades" />
        </el-form-item>
    </el-form>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="handleGenerate">生成</el-button>
      </span>
    </template>
  </el-dialog>
</template>
