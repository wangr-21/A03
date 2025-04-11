<script setup lang="ts">
import { ref, reactive } from 'vue';
import type { FormInstance, FormRules, UploadRequestOptions } from 'element-plus';
import { ElMessage } from 'element-plus';
import {
  User,
  Key,
  Phone,
  Message,
  Check,
  UserFilled,
  Document,
  Plus,
} from '@element-plus/icons-vue';
import type { Student } from '@/api';

defineProps<{
  classOptions: { label: string; value: string }[];
}>();

const visible = defineModel<boolean>('visible');

const emit = defineEmits<{
  submit: [studentData: Student];
}>();

const formRef = ref<FormInstance>();
const submitting = ref(false);

// 年级选项
const grades = [
  { label: '七年级', value: '7' },
  { label: '八年级', value: '8' },
  { label: '九年级', value: '9' },
];

// 表单数据
const form = reactive({
  name: '',
  id: '',
  grade: '',
  class: '',
  avatar: '',
  introduction: '',
  phone: '',
  email: '',
});

// 表单验证规则
const rules = reactive<FormRules>({
  name: [
    { required: true, message: '请输入学生姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '长度应在 2 到 20 个字符之间', trigger: 'blur' },
  ],
  id: [
    { required: true, message: '请输入学号', trigger: 'blur' },
    { pattern: /^\d{8,12}$/, message: '请输入8-12位数字学号', trigger: 'blur' },
  ],
  grade: [{ required: true, message: '请选择年级', trigger: 'change' }],
  class: [{ required: true, message: '请选择班级', trigger: 'change' }],
  phone: [{ pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }],
  email: [{ type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }],
});

// 头像上传前的验证
const beforeAvatarUpload = (file: File) => {
  if (!file.type.startsWith('image/')) {
    ElMessage.error('头像必须是图片格式!');
    return false;
  }
  if (file.size / 1024 / 1024 > 2) {
    ElMessage.error('头像大小不能超过 2MB!');
    return false;
  }
  return true;
};

// 处理头像上传
const handleAvatarUpload = async (options: UploadRequestOptions) => {
  const file = options.file;
  // 这里应该调用实际的上传API
  // 现在使用本地URL模拟
  form.avatar = URL.createObjectURL(file);
};

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return;

  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true;
      try {
        // 这里应该调用实际的API
        await new Promise((resolve) => setTimeout(resolve, 1000));

        emit('submit', { ...form } as unknown as Student);
        ElMessage.success('学生信息添加成功！');
        closeDialog();
      } catch (error) {
        console.error('添加学生失败:', error);
        ElMessage.error('添加学生失败，请重试');
      } finally {
        submitting.value = false;
      }
    }
  });
};

// 关闭对话框
const closeDialog = () => {
  formRef.value?.resetFields();
  form.avatar = '';
  visible.value = false;
};
</script>

<template>
  <el-dialog
    title="迎新引航"
    :model-value="visible"
    @update:model-value="visible = $event"
    width="600px"
    class="add-student-dialog"
    :close-on-click-modal="false"
  >
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-position="top"
      class="add-student-form"
    >
      <!-- 基本信息部分 -->
      <div class="form-section">
        <div class="section-title">
          <el-icon><UserFilled /></el-icon>
          <span>基本信息</span>
        </div>

        <div class="form-row">
          <el-form-item label="学生姓名" prop="name" class="form-item">
            <el-input v-model="form.name" placeholder="请输入学生姓名" :prefix-icon="User" />
          </el-form-item>

          <el-form-item label="学号" prop="id" class="form-item">
            <el-input v-model="form.id" placeholder="请输入学号" :prefix-icon="Key" />
          </el-form-item>
        </div>

        <div class="form-row">
          <el-form-item label="年级" prop="grade" class="form-item">
            <el-select v-model="form.grade" placeholder="请选择年级" class="full-width">
              <el-option
                v-for="grade in grades"
                :key="grade.value"
                :label="grade.label"
                :value="grade.value"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="班级" prop="class" class="form-item">
            <el-select v-model="form.class" placeholder="请选择班级" class="full-width">
              <el-option
                v-for="option in classOptions"
                :key="option.value"
                :label="option.label"
                :value="option.value"
              />
            </el-select>
          </el-form-item>
        </div>
      </div>

      <!-- 个人档案部分 -->
      <div class="form-section">
        <div class="section-title">
          <el-icon><Document /></el-icon>
          <span>个人档案</span>
        </div>

        <div class="avatar-upload">
          <el-upload
            class="avatar-uploader"
            action="#"
            :show-file-list="false"
            :before-upload="beforeAvatarUpload"
            :http-request="handleAvatarUpload"
          >
            <img v-if="form.avatar" :src="form.avatar" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
          <div class="upload-tip">点击上传头像</div>
        </div>

        <el-form-item label="个人简介" prop="introduction">
          <el-input
            v-model="form.introduction"
            type="textarea"
            :rows="3"
            placeholder="请输入学生的个人简介（选填）"
          />
        </el-form-item>
      </div>

      <!-- 联系方式部分 -->
      <div class="form-section">
        <div class="section-title">
          <el-icon><Phone /></el-icon>
          <span>联系方式</span>
        </div>

        <div class="form-row">
          <el-form-item label="联系电话" prop="phone" class="form-item">
            <el-input v-model="form.phone" placeholder="请输入联系电话" :prefix-icon="Phone" />
          </el-form-item>

          <el-form-item label="电子邮箱" prop="email" class="form-item">
            <el-input v-model="form.email" placeholder="请输入电子邮箱" :prefix-icon="Message" />
          </el-form-item>
        </div>
      </div>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="closeDialog">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">
          <el-icon class="submit-icon"><Check /></el-icon>
          添加学生
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>
.add-student-dialog :deep(.el-dialog__body) {
  padding: 20px 30px;
}

.add-student-form {
  max-height: 60vh;
  overflow-y: auto;
  padding-right: 10px;
}

.add-student-form::-webkit-scrollbar {
  width: 6px;
}

.add-student-form::-webkit-scrollbar-thumb {
  background-color: #dcdfe6;
  border-radius: 3px;
}

.form-section {
  background: var(--el-fill-color-light);
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin-bottom: 20px;
}

.form-row {
  display: flex;
  gap: 20px;
}

.form-item {
  flex: 1;
}

.full-width {
  width: 100%;
}

.avatar-upload {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.avatar-uploader {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration);
}

.avatar-uploader:hover {
  border-color: var(--el-color-primary);
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  text-align: center;
  line-height: 100px;
}

.avatar {
  width: 100px;
  height: 100px;
  display: block;
  object-fit: cover;
}

.upload-tip {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  margin-top: 8px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 20px;
}

.submit-icon {
  margin-right: 4px;
}

@keyframes slide-fade {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.form-section {
  animation: slide-fade 0.3s ease-out;
}

@media screen and (max-width: 768px) {
  .form-row {
    flex-direction: column;
    gap: 0;
  }

  .add-student-dialog :deep(.el-dialog) {
    width: 90% !important;
    max-width: none;
  }
}
</style>
