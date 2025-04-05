<script setup lang="ts">
defineProps<{
  tools: Array<{
    title: string;
    description: string;
    icon: string;
    color: string;
    buttonText: string;
    buttonType: 'primary' | 'warning' | 'info' | 'success' | 'danger' | 'default';
  }>;
}>();

// 定义工具卡片点击事件
const emit = defineEmits<{
  toolClicked: [toolTitle: string];
}>();

const handleToolClick = (toolTitle: string) => {
  emit('toolClicked', toolTitle);
};
</script>

<template>
  <div class="tool-cards">
    <el-card class="tool-card" v-for="(tool, index) in tools" :key="index">
      <div class="tool-icon">
        <el-icon :size="40" :color="tool.color">
          <component :is="tool.icon" />
        </el-icon>
      </div>
      <h3 class="tool-title">{{ tool.title }}</h3>
      <p class="tool-desc">{{ tool.description }}</p>
      <el-button class="tool-btn" :type="tool.buttonType" @click="handleToolClick(tool.title)">
        {{ tool.buttonText }}
      </el-button>
    </el-card>
  </div>
</template>

<style scoped>
.tool-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.tool-card {
  text-align: center;
  padding: 30px 20px;
  transition: all 0.3s ease;
}

.tool-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.tool-icon {
  margin-bottom: 15px;
}

.tool-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

.tool-desc {
  color: #666;
  margin-bottom: 20px;
  height: 60px;
}

.tool-btn {
  width: 100%;
}
</style>
