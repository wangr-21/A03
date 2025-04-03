<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { getCases } from '@/api';
import type { CaseItem, CaseFilters } from '@/api';

// --- State for 时空走廊 ---
const caseFilters = reactive<CaseFilters>({
  category: '', // e.g., '传统故事', '跨学科案例'
  era: '', // e.g., '唐代', '宋代'
  theme: '',
});
const caseCategories = ref<string[]>(['传统故事', '跨学科案例']);
const eras = ref<string[]>(['先秦', '秦汉', '魏晋', '隋唐', '宋元', '明清']); // Placeholder
const themes = ref<string[]>(['爱国主义', '科学探索', '文化艺术', '哲学思辨']); // Placeholder
const cases = ref<CaseItem[]>([]); // Will hold fetched cases
const isCasesLoading = ref<boolean>(false);

const filterCases = async (): Promise<void> => {
  console.log('Filtering cases:', caseFilters);
  isCasesLoading.value = true;

  try {
    const response = await getCases(caseFilters);

    if (response.success) {
      cases.value = response.data.cases;
    } else {
      throw new Error('Failed to fetch cases');
    }
  } catch (error) {
    console.error('Error filtering cases:', error);
    ElMessage.error('获取案例失败，请稍后重试');
    cases.value = [];
  } finally {
    isCasesLoading.value = false;
  }
};

const viewCaseDetails = (caseId: number): void => {
  console.log('Viewing case details:', caseId);
  // TODO: Navigate to case detail page or open modal
  ElMessage.info('Not implemented yet: ' + caseId);
};

// Initial data fetch on mount
onMounted(() => {
  filterCases();
});
</script>

<template>
  <el-card class="case-library-card">
    <template #header>
      <div class="card-header">
        <h3>
          <el-icon><Clock /></el-icon> 时空走廊 - 故事与案例
        </h3>
      </div>
    </template>

    <!-- Filters -->
    <div class="filters">
      <el-form :inline="true" :model="caseFilters">
        <el-form-item label="分类">
          <el-select v-model="caseFilters.category" placeholder="选择分类" clearable size="small">
            <el-option v-for="c in caseCategories" :key="c" :label="c" :value="c"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="朝代/时期">
          <el-select v-model="caseFilters.era" placeholder="选择朝代/时期" clearable size="small">
            <el-option v-for="e in eras" :key="e" :label="e" :value="e"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="主题">
          <el-select v-model="caseFilters.theme" placeholder="选择主题" clearable size="small">
            <el-option v-for="t in themes" :key="t" :label="t" :value="t"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="filterCases" icon="Search" size="small"
            >筛选案例</el-button
          >
        </el-form-item>
      </el-form>
    </div>

    <!-- Case List (Cards) -->
    <div class="case-list" v-loading="isCasesLoading">
      <el-card shadow="hover" v-for="item in cases" :key="item.id" class="case-card">
        <template #header>
          <div class="card-header">
            <span>{{ item.title }}</span>
            <el-tag size="small">{{ item.category }}</el-tag>
          </div>
        </template>
        <p class="case-summary">{{ item.summary || '暂无简介...' }}</p>
        <div class="case-footer">
          <el-tag type="info" size="small" v-if="item.era">{{ item.era }}</el-tag>
          <el-tag type="warning" size="small" v-if="item.theme">{{ item.theme }}</el-tag>
          <el-button text type="primary" @click="viewCaseDetails(item.id)">查看详情</el-button>
        </div>
      </el-card>
      <el-empty
        v-if="!isCasesLoading && cases.length === 0"
        description="暂无案例，请调整筛选条件"
      ></el-empty>
    </div>
  </el-card>
</template>

<style scoped>
.case-library-card {
  margin-bottom: 30px;
}

.filters {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.filters .el-form-item {
  margin-bottom: 10px; /* Adjust spacing for inline form */
}

.case-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  min-height: 100px; /* Ensure loading is visible */
}

.case-card .card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.case-summary {
  color: #666;
  font-size: 14px;
  margin-bottom: 15px;
  min-height: 40px; /* Ensure consistent height */
}

.case-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #f0f0f0;
  padding-top: 10px;
  margin-top: 10px;
}

.case-footer .el-tag {
  margin-right: 5px;
}
</style>
