<template>
  <div class="lesson-plan-form">
    <div class="form-header">
      <h2>{{ isEdit ? '编辑课程计划' : '新建课程计划' }}</h2>
    </div>
    
    <el-form 
      ref="formRef" 
      :model="form" 
      :rules="rules" 
      label-width="100px" 
      v-loading="loading"
    >
      <el-form-item label="课程标题" prop="title">
        <el-input v-model="form.title" placeholder="请输入课程标题" />
      </el-form-item>
      
      <el-form-item label="课程描述" prop="description">
        <el-input 
          v-model="form.description" 
          type="textarea" 
          :rows="3" 
          placeholder="请输入课程描述"
        />
      </el-form-item>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="学科" prop="subject">
            <el-select v-model="form.subject" placeholder="请选择学科" style="width: 100%">
              <el-option label="美术" value="美术" />
              <el-option label="音乐" value="音乐" />
              <el-option label="体育" value="体育" />
              <el-option label="综合实践" value="综合实践" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="年级" prop="grade">
            <el-select v-model="form.grade" placeholder="请选择年级" style="width: 100%">
              <el-option 
                v-for="grade in grades" 
                :key="grade" 
                :label="grade" 
                :value="grade" 
              />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="课时" prop="duration">
            <el-input-number 
              v-model="form.duration" 
              :min="1" 
              :max="180" 
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-form-item label="教学目标" prop="objectives">
        <div class="objectives-container">
          <div 
            v-for="(objective, index) in form.objectives" 
            :key="index" 
            class="objective-item"
          >
            <el-input v-model="form.objectives[index]" placeholder="请输入教学目标" />
            <el-button 
              type="danger" 
              circle 
              icon="el-icon-delete" 
              size="mini" 
              @click="removeObjective(index)"
            />
          </div>
          <el-button type="primary" @click="addObjective">添加教学目标</el-button>
        </div>
      </el-form-item>
      
      <el-form-item label="课程内容" prop="content">
        <el-input 
          v-model="form.content" 
          type="textarea" 
          :rows="8" 
          placeholder="请输入课程内容"
        />
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="submitForm">保存</el-button>
        <el-button @click="cancel">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { getLessonPlan, createLessonPlan, updateLessonPlan } from '@/api/workshop';
import { ElMessage } from 'element-plus';

const router = useRouter();
const route = useRoute();
const formRef = ref(null);
const loading = ref(false);

// 判断是否为编辑模式
const isEdit = computed(() => !!route.params.id);

// 年级选项
const grades = [
  '一年级', '二年级', '三年级', '四年级', '五年级', '六年级',
  '初一', '初二', '初三', '高一', '高二', '高三'
];

// 表单数据
const form = reactive({
  title: '',
  description: '',
  subject: '美术',
  grade: '',
  duration: 45,
  objectives: [''],
  content: ''
});

// 表单验证规则
const rules = {
  title: [
    { required: true, message: '请输入课程标题', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入课程描述', trigger: 'blur' }
  ],
  subject: [
    { required: true, message: '请选择学科', trigger: 'change' }
  ],
  grade: [
    { required: true, message: '请选择年级', trigger: 'change' }
  ],
  duration: [
    { required: true, message: '请输入课时', trigger: 'blur' },
    { type: 'number', message: '课时必须为数字' }
  ],
  content: [
    { required: true, message: '请输入课程内容', trigger: 'blur' }
  ]
};

// 添加教学目标
const addObjective = () => {
  form.objectives.push('');
};

// 删除教学目标
const removeObjective = (index) => {
  form.objectives.splice(index, 1);
  // 确保至少有一个目标
  if (form.objectives.length === 0) {
    form.objectives.push('');
  }
};

// 加载课程计划数据（编辑模式）
const loadLessonPlan = async () => {
  if (!isEdit.value) return;
  
  loading.value = true;
  try {
    const response = await getLessonPlan(route.params.id);
    const plan = response.data;
    
    // 更新表单数据
    Object.keys(form).forEach(key => {
      if (plan[key] !== undefined) {
        form[key] = plan[key];
      }
    });
    
    // 确保 objectives 是数组
    if (!Array.isArray(form.objectives) || form.objectives.length === 0) {
      form.objectives = [''];
    }
  } catch (error) {
    ElMessage.error('获取课程计划数据失败');
    console.error(error);
  } finally {
    loading.value = false;
  }
};

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return;
  
  await formRef.value.validate(async (valid) => {
    if (!valid) {
      ElMessage.warning('请完善表单信息');
      return;
    }
    
    loading.value = true;
    try {
      // 过滤空的教学目标
      const formData = { ...form };
      formData.objectives = formData.objectives.filter(obj => obj.trim() !== '');
      
      if (isEdit.value) {
        await updateLessonPlan(route.params.id, formData);
        ElMessage.success('更新成功');
      } else {
        await createLessonPlan(formData);
        ElMessage.success('创建成功');
      }
      
      // 返回列表页
      router.push({ name: 'lesson-plans' });
    } catch (error) {
      ElMessage.error(isEdit.value ? '更新失败' : '创建失败');
      console.error(error);
    } finally {
      loading.value = false;
    }
  });
};

// 取消
const cancel = () => {
  router.back();
};

onMounted(() => {
  loadLessonPlan();
});
</script>

<style scoped>
.lesson-plan-form {
  padding: 20px;
  max-width: 900px;
  margin: 0 auto;
}

.form-header {
  margin-bottom: 30px;
}

.objectives-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.objective-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.el-input-number {
  width: 100%;
}
</style> 