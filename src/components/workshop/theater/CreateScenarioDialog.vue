<script setup lang="ts">
import { reactive } from 'vue';
import type { CreateScenarioRequest } from '@/api/thinking';

const visible = defineModel<boolean>('visible', { required: true });

const emit = defineEmits<{
  submit: [data: CreateScenarioRequest];
}>();

const formData = reactive<CreateScenarioRequest>({
  scenario_type: 'literary',
  subject: '语文',
  grade: '七年级',
  theme: '',
});

// 场景类型选项
const scenarioTypes = [
  { value: 'historical', label: '历史情境' },
  { value: 'literary', label: '文学情境' },
  { value: 'scientific', label: '科学情境' },
];

// 学科选项
const subjects = ['语文', '数学', '英语', '科学'];

// 年级选项
const grades = ['七年级', '八年级', '九年级'];

const handleSubmit = () => {
  emit('submit', { ...formData });
  visible.value = false;
};

const handleCancel = () => {
  visible.value = false;
};
</script>

<template>
  <el-dialog title="创建情景模拟" v-model="visible" width="500px" @close="handleCancel">
    <el-form :model="formData" label-width="80px">
      <el-form-item label="场景类型">
        <el-select v-model="formData.scenario_type" class="w-full">
          <el-option
            v-for="type in scenarioTypes"
            :key="type.value"
            :label="type.label"
            :value="type.value"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="学科">
        <el-select v-model="formData.subject" class="w-full">
          <el-option v-for="subject in subjects" :key="subject" :label="subject" :value="subject" />
        </el-select>
      </el-form-item>

      <el-form-item label="年级">
        <el-select v-model="formData.grade" class="w-full">
          <el-option v-for="grade in grades" :key="grade" :label="grade" :value="grade" />
        </el-select>
      </el-form-item>

      <el-form-item label="主题">
        <el-input v-model="formData.theme" placeholder="请输入场景主题" />
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确认创建</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>
.w-full {
  width: 100%;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
