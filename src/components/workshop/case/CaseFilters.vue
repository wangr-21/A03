<script setup lang="ts">
import { reactive } from 'vue';
import type { DisciplineCategory, CaseFilters } from '@/api';

defineProps<{
  disciplines: DisciplineCategory[];
}>();

const emit = defineEmits<{
  filter: [filters: CaseFilters];
}>();

const filters = reactive<CaseFilters>({
  story_id: undefined,
  main_discipline: undefined,
  related_discipline: undefined,
  suitable_grade: undefined,
});

const handleFilter = () => {
  emit('filter', { ...filters });
};
</script>

<template>
  <div class="filters">
    <el-form :inline="true" :model="filters">
      <el-form-item label="主要学科" style="width: 20%">
        <el-select v-model="filters.main_discipline" clearable>
          <el-option
            v-for="discipline in disciplines"
            :key="discipline.name"
            :label="discipline.name"
            :value="discipline.name"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="相关学科" style="width: 20%">
        <el-select v-model="filters.related_discipline" clearable>
          <el-option
            v-for="discipline in disciplines"
            :key="discipline.name"
            :label="discipline.name"
            :value="discipline.name"
          />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleFilter">筛选</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<style scoped>
.filters {
  margin-bottom: 20px;
}
</style>
