<script setup lang="ts">
import { reactive } from 'vue';
import type { DynastyInfo, ThemeCategory, StoryFilters } from '@/api';

defineProps<{
  dynasties: DynastyInfo[];
  themes: ThemeCategory[];
}>();

const emit = defineEmits<{
  filter: [filters: StoryFilters];
}>();

const filters = reactive<StoryFilters>({
  dynasty: undefined,
  theme: undefined,
  keyword: undefined,
});

const handleFilter = () => {
  emit('filter', { ...filters });
};
</script>

<template>
  <div class="filters">
    <el-form :inline="true" :model="filters">
      <el-form-item label="朝代" style="width: 15%">
        <el-select v-model="filters.dynasty" clearable>
          <el-option
            v-for="dynasty in dynasties"
            :key="dynasty.name"
            :label="dynasty.name"
            :value="dynasty.name"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="主题" style="width: 20%">
        <el-select v-model="filters.theme" clearable>
          <el-option
            v-for="theme in themes"
            :key="theme.name"
            :label="theme.name"
            :value="theme.name"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="关键词" style="width: 30%">
        <el-input v-model="filters.keyword" clearable />
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
