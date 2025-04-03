<script setup lang="ts">
const emit = defineEmits(['open-dialog']);

const openPostDialog = () => {
  emit('open-dialog');
};
</script>

<template>
  <el-card class="post-creator-card simple">
    <div @click="openPostDialog" class="creator-placeholder">
      <el-avatar size="small" src="/src/assets/my_avatar.svg"></el-avatar>
      <span>分享您的教学经验、资源或创意...</span>
    </div>
    <div class="creator-actions simple">
      <el-button text @click="openPostDialog">
        <el-icon><Picture /></el-icon>图片
      </el-button>
      <el-button text @click="openPostDialog">
        <el-icon><Paperclip /></el-icon>附件
      </el-button>
      <el-button text @click="openPostDialog">
        <el-icon><CollectionTag /></el-icon>话题
      </el-button>
    </div>
  </el-card>
</template>

<style scoped>
.post-creator-card.simple {
  padding: 15px;
  cursor: pointer;
}

.creator-placeholder {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #999;
  padding: 12px;
  border: 1px solid #eee;
  border-radius: 8px;
  margin-bottom: 10px;
  transition: all 0.3s ease;
}

.creator-placeholder:hover {
  background-color: #f8f9fa;
  border-color: #dcdfe6;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.creator-actions.simple {
  justify-content: flex-start;
  gap: 20px;
  margin-top: 0;
}

.creator-actions.simple .el-button {
  color: #666;
  transition: color 0.3s ease;
}

.creator-actions.simple .el-button:hover {
  color: #409eff;
}
</style>
