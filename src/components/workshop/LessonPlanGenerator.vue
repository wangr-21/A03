<script setup lang="ts">
import { ref, reactive } from 'vue';
import { ElMessage, type UploadFile, type UploadFiles } from 'element-plus';
import MarkdownIt from 'markdown-it';
import { generateLessonPlan, exportPlanAsDocx } from '@/api';

const md = new MarkdownIt();

// Reactive form data
const planForm = reactive({
  grade: '',
  teachingInspiration: '',
});

// 文件上传相关
const grades = ref<string[]>(['初一', '初二', '初三']);
const uploadedImages = ref<UploadFile[]>([]);
const planId = ref<string | null>(null);
const isExporting = ref<boolean>(false);
const isGenerating = ref<boolean>(false);
const generatedPlan = ref<string | null>(null);

const handlePlanImageChange = (file: UploadFile, files: UploadFiles) => {
  // 验证文件类型
  const isImage = ['image/jpeg', 'image/png', 'image/gif'].includes(file.raw?.type || 'unknown');
  if (!isImage) {
    ElMessage.error('只能上传图片文件!');
    return false;
  }

  // 验证文件大小（示例限制5MB）
  const isLt5M = (file.raw?.size || 0) / 1024 / 1024 < 5;
  if (!isLt5M) {
    ElMessage.error('图片大小不能超过5MB!');
    return false;
  }

  uploadedImages.value = files;
};

const handleRemoveImage = (file: UploadFile) => {
  uploadedImages.value = uploadedImages.value.filter((f) => f.uid !== file.uid);
};

// 生成教案
const generateLessonPlanFunc = async (): Promise<void> => {
  if (!planForm.grade || uploadedImages.value.length === 0 || !planForm.teachingInspiration) {
    ElMessage.warning('请填写完整信息（年级、教材图片和教学灵感）！');
    return;
  }

  isGenerating.value = true;
  generatedPlan.value = null; // 清除之前的结果

  try {
    // 提取上传的文件
    const imageFiles = uploadedImages.value
      .map((file) => file.raw)
      .filter((file) => file !== undefined) as File[];

    // 调用API模块中的函数
    const result = await generateLessonPlan(
      planForm.grade,
      imageFiles,
      // planForm.teachingInspiration,  // 后端未实现
    );

    // 存储计划ID用于后续导出
    planId.value = result.plan_id;
    // 使用 markdown-it 渲染 Markdown 内容
    generatedPlan.value = md.render(result.plan);
    ElMessage.success('教案生成成功！');
  } catch (error) {
    console.error('Error generating lesson plan:', error);
    ElMessage.error('教案生成失败，请稍后重试。');
  } finally {
    isGenerating.value = false;
  }
};

// 导出为Word文档
const exportPlanAsDocxFunc = async (): Promise<void> => {
  if (!planId.value) return;

  isExporting.value = true;

  try {
    // 调用API模块中的函数
    const blob = await exportPlanAsDocx(planId.value);

    // 下载文件
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `教案_${planId.value}.docx`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    ElMessage.success('教案导出成功！');
  } catch (error) {
    console.error('Error exporting document:', error);
    ElMessage.error('教案导出失败，请稍后重试。');
  } finally {
    isExporting.value = false;
  }
};
</script>

<template>
  <div>
    <!-- 灵犀教案 - 生成区域 -->
    <el-card class="generator-card">
      <template #header>
        <div class="card-header">
          <h3>
            <el-icon><EditPen /></el-icon> 灵犀教案生成器
          </h3>
        </div>
      </template>
      <el-form :model="planForm" label-width="100px" class="generator-form">
        <el-form-item label="年级" required>
          <el-select v-model="planForm.grade" placeholder="请选择年级">
            <el-option v-for="item in grades" :key="item" :label="item" :value="item"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="教学灵感" required>
          <el-input
            v-model="planForm.teachingInspiration"
            type="textarea"
            :rows="3"
            placeholder="请描述您的教学构想，例如：希望通过生动的实验演示来讲解光的折射原理，让学生能够直观理解并产生兴趣..."
          ></el-input>
          <div class="inspiration-tips">
            <el-icon><InfoFilled /></el-icon>
            提示：描述越具体，生成的教案就越符合您的期望。可以包含教学目标、重点难点、教学方法等。
          </div>
        </el-form-item>

        <el-form-item label="教材图片" required>
          <el-upload
            class="upload-demo"
            action="#"
            :on-remove="handleRemoveImage"
            :on-change="handlePlanImageChange"
            :file-list="uploadedImages"
            :limit="5"
            multiple
            :auto-upload="false"
            list-type="picture-card"
          >
            <el-icon><Plus /></el-icon>
            <template #tip>
              <div class="el-upload__tip">请上传教材内容图片，支持多图上传（最多5张）</div>
            </template>
          </el-upload>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            @click="generateLessonPlanFunc"
            :loading="isGenerating"
            icon="MagicStick"
            :disabled="
              !planForm.grade || uploadedImages.length === 0 || !planForm.teachingInspiration
            "
          >
            {{ isGenerating ? '正在生成...' : '智能生成教案' }}
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 灵犀教案 - 展示区域 -->
    <el-card class="display-card" v-if="generatedPlan || isGenerating">
      <template #header>
        <div class="card-header">
          <h3>
            <el-icon><Document /></el-icon> 生成结果
          </h3>
          <div>
            <el-button
              type="primary"
              size="small"
              :disabled="!planId || isExporting"
              @click="exportPlanAsDocxFunc"
              :loading="isExporting"
            >
              <el-icon><Download /></el-icon>
              {{ isExporting ? '导出中...' : '导出Word文档' }}
            </el-button>
          </div>
        </div>
      </template>
      <div v-if="isGenerating" class="loading-placeholder">
        <el-skeleton :rows="10" animated />
      </div>
      <div v-else-if="generatedPlan" class="generated-content" v-html="generatedPlan"></div>
    </el-card>
  </div>
</template>

<style scoped>
.generator-card,
.display-card {
  margin-bottom: 30px;
}

.generator-form .el-select {
  width: 100%; /* Make select boxes fill column */
}

.display-card .card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.display-card .card-header h3 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 5px;
}

.loading-placeholder {
  padding: 20px;
}

.generated-content {
  line-height: 1.8;
  font-family: 'KaiTi', 'Times New Roman', serif;
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 4px;
  background-color: #fdfdfd;
}

/* Markdown 样式 */
.generated-content :deep(h1),
.generated-content :deep(h2),
.generated-content :deep(h3),
.generated-content :deep(h4),
.generated-content :deep(h5),
.generated-content :deep(h6) {
  margin-top: 1em;
  margin-bottom: 0.5em;
  font-weight: bold;
}

.generated-content :deep(h1) {
  font-size: 1.5em;
}

.generated-content :deep(h2) {
  font-size: 1.3em;
}

.generated-content :deep(h3) {
  font-size: 1.2em;
}

.generated-content :deep(p) {
  margin-bottom: 1em;
}

.generated-content :deep(ul),
.generated-content :deep(ol) {
  padding-left: 2em;
  margin-bottom: 1em;
}

.generated-content :deep(li) {
  margin-bottom: 0.5em;
}

.generated-content :deep(strong) {
  font-weight: bold;
}

.generated-content :deep(em) {
  font-style: italic;
}

.generated-content :deep(blockquote) {
  border-left: 4px solid #ddd;
  padding-left: 1em;
  color: #666;
  margin-bottom: 1em;
}

.generated-content :deep(code) {
  background-color: #f5f5f5;
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-family: Consolas, Monaco, monospace;
}

.generated-content :deep(pre) {
  background-color: #f5f5f5;
  padding: 1em;
  border-radius: 5px;
  overflow-x: auto;
  margin-bottom: 1em;
}

.generated-content :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin-bottom: 1em;
}

.generated-content :deep(th),
.generated-content :deep(td) {
  border: 1px solid #ddd;
  padding: 0.5em;
  text-align: left;
}

.generated-content :deep(th) {
  background-color: #f5f5f5;
}

.inspiration-tips {
  margin-top: 8px;
  font-size: 12px;
  color: #909399;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px;
  background-color: #f8f9fa;
  border-radius: 4px;
  line-height: 1.4;
}

.inspiration-tips :deep(.el-icon) {
  color: #409eff;
  font-size: 14px;
}
</style>
