<script setup lang="ts">
import { reactive } from 'vue';
import type { CreateActivityRequest } from '@/api/thinking';

const visible = defineModel<boolean>('visible', { required: true });

const emit = defineEmits<{
  submit: [data: CreateActivityRequest];
}>();

const formData = reactive<CreateActivityRequest>({
  activity_type: 'discussion',
  subject: '语文',
  grade: '七年级',
  topic: '',
  duration: 45,
});

// 活动类型选项
const activityTypes = [
  { value: 'discussion', label: '讨论' },
  { value: 'question', label: '提问' },
  { value: 'game', label: '游戏' },
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
  <el-dialog title="创建互动活动" v-model="visible" width="500px" @close="handleCancel">
    <el-form :model="formData" label-width="80px">
      <el-form-item label="活动类型">
        <el-select v-model="formData.activity_type" class="w-full">
          <el-option
            v-for="type in activityTypes"
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

      <el-form-item label="活动主题">
        <el-input v-model="formData.topic" placeholder="请输入活动主题" />
      </el-form-item>

      <el-form-item label="时长(分)">
        <el-input-number
          v-model="formData.duration"
          :min="15"
          :max="120"
          :step="5"
          class="w-duration"
        />
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

.w-duration {
  width: 30%;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
