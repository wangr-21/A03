<script setup lang="ts">
import type { CaseItem } from '@/api';

defineProps<{
  case_: CaseItem;
}>();

const emit = defineEmits<{
  detail: [case_: CaseItem];
}>();
</script>

<template>
  <el-card class="case-card" shadow="hover" @click="emit('detail', case_)">
    <template #header>
      <div class="card-header">
        <span class="title">{{ case_.title }}</span>
        <el-tag size="small">{{ case_.main_discipline }}</el-tag>
      </div>
    </template>

    <div class="card-preview">
      <!-- 简要教学目标 -->
      <p class="objectives-preview">{{ case_.teaching_objectives.substring(0, 50) }}...</p>

      <!-- 标签展示 -->
      <div class="preview-tags">
        <el-tag size="small" type="info" class="preview-tag">{{ case_.suitable_grades }}</el-tag>
        <el-tag size="small" type="warning" class="preview-tag">{{
          case_.related_disciplines
        }}</el-tag>
      </div>

      <!-- 资源预览 -->
      <div v-if="case_.resources?.length" class="preview-resources">
        <el-tag size="small" type="success"> {{ case_.resources.length }} 个教学资源 </el-tag>
      </div>
    </div>
  </el-card>
</template>

<style scoped>
.case-card {
  cursor: pointer;
  transition: transform 0.2s;
  height: 100%;
  display: flex;
  flex-direction: column;

  &:hover {
    transform: translateY(-5px);
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;

  .title {
    font-weight: bold;
    font-size: 1.1em;
    color: #303133;
  }
}

.card-preview {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;

  .objectives-preview {
    color: #606266;
    margin: 0;
    font-size: 0.9em;
    display: -webkit-box;
    line-clamp: 2;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .preview-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: auto;
  }

  .preview-resources {
    display: flex;
    justify-content: flex-end;
    margin-top: 8px;
  }
}

:deep(.el-card__body) {
  flex: 1;
  display: flex;
  flex-direction: column;
}
</style>
