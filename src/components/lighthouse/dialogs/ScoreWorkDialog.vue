<template>
  <el-dialog
    :model-value="modelValue"
    @update:model-value="emit('update:modelValue')"
    title="星光成长档案"
    width="500px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <el-form :model="form" ref="formRef" :rules="rules" label-width="80px">
      <el-form-item label="学生姓名" prop="studentName">
        <el-input v-model="form.studentName" disabled></el-input>
      </el-form-item>
      <el-form-item label="成绩" prop="score">
        <el-input-number 
          v-model="form.score" 
          :min="0" 
          :max="100" 
          :precision="1"
          :step="0.5"
          style="width: 150px"
        ></el-input-number>
      </el-form-item>
      <el-form-item label="评语" prop="comment">
        <el-input
          v-model="form.comment"
          type="textarea"
          :rows="3"
          placeholder="请输入对学生的点评和建议..."
        ></el-input>
        <div class="comment-tips">
          <i class="el-icon-info-filled"></i> 
          评语可以包含学生的进步、优势、建议以及鼓励的话语，帮助学生发掘潜能。
        </div>
      </el-form-item>
      <el-form-item label="作品" prop="work">
        <el-upload
          class="upload-demo"
          action="/api/upload"
          :on-preview="handlePreview"
          :on-remove="handleRemove"
          :before-remove="beforeRemove"
          multiple
          :limit="3"
          :on-exceed="handleExceed"
          :file-list="fileList"
        >
          <el-button type="primary">点击上传</el-button>
          <template #tip>
            <div class="el-upload__tip">
              支持jpg/png/pdf文件，且不超过10mb
            </div>
          </template>
        </el-upload>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleSubmit">
          确认
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import type { UploadProps, UploadUserFile } from 'element-plus'
import { ElMessage, ElMessageBox } from 'element-plus'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  student: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'submit'])

const formRef = ref()
const form = ref({
  studentName: '',
  score: 0,
  comment: '',
  work: []
})

const rules = {
  score: [
    { required: true, message: '请输入成绩', trigger: 'blur' },
    { type: 'number', min: 0, max: 100, message: '成绩必须在0-100之间', trigger: 'blur' }
  ],
  comment: [
    { max: 500, message: '评语不能超过500个字符', trigger: 'blur' }
  ]
}

const fileList = ref<UploadUserFile[]>([])

watch(() => props.student, (newVal) => {
  if (newVal) {
    form.value.studentName = newVal.name || ''
    form.value.score = newVal.score || 0
    // 如果有已有的作品文件，可以在这里设置 fileList
  }
}, { immediate: true })

const handleClose = () => {
  emit('update:modelValue', false)
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate((valid: boolean) => {
    if (valid) {
      emit('submit', {
        ...form.value,
        files: fileList.value
      })
      handleClose()
    }
  })
}

const handleExceed: UploadProps['onExceed'] = (files) => {
  ElMessage.warning(
    `当前限制选择 3 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.value.length} 个文件`
  )
}

const handleRemove: UploadProps['onRemove'] = (file, uploadFiles) => {
  console.log(file, uploadFiles)
}

const handlePreview: UploadProps['onPreview'] = (uploadFile) => {
  console.log(uploadFile)
}

const beforeRemove: UploadProps['beforeRemove'] = (uploadFile) => {
  return ElMessageBox.confirm(
    `确定移除 ${uploadFile.name}？`
  ).then(
    () => true,
    () => false
  )
}
</script>

<style scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.comment-tips {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
  padding: 5px 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
  line-height: 1.5;
}
</style> 