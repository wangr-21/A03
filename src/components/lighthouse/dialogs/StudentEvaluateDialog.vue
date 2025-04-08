<script setup lang="ts">
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import type { Student } from '@/api';

defineProps<{
  student: Student | null;
  submitting: boolean;
}>();

const visible = defineModel('visible', { required: true });

const emit = defineEmits<{
  submit: [content: string];
}>();

const evaluationContent = ref('');

const closeDialog = () => {
  visible.value = false;
};

const submitEvaluation = async () => {
  if (!evaluationContent.value.trim()) {
    ElMessage.warning('请输入评价内容');
    return;
  }

  emit('submit', evaluationContent.value);
};
</script>

<template>
  <el-dialog
    v-model="visible"
    @update:model-value="(val: boolean) => (visible = val)"
    :title="`评价学生 - ${student?.name}`"
    width="500px"
  >
    <div v-if="student" class="student-evaluate">
      <p>学号: {{ student.id }} | 班级: {{ student.grade }}{{ student.class }}</p>
      <el-form>
        <el-form-item label="教师评价">
          <el-input
            v-model="evaluationContent"
            type="textarea"
            rows="4"
            placeholder="请输入对该学生的评价内容..."
          />
        </el-form-item>
      </el-form>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="closeDialog">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submitEvaluation">
          提交评价
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<style scoped>
.student-evaluate {
  margin-bottom: 20px;
}
</style>
