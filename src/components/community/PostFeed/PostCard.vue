<script setup lang="ts">
import type { Post } from '@/api';

defineProps<{
  post: Post;
}>();
</script>

<template>
  <el-card class="post-card">
    <div class="post-header">
      <el-avatar :size="40" :src="post.author.avatar"></el-avatar>
      <div class="author-info">
        <span class="author-name">{{ post.author.name }}</span>
        <span class="post-meta">{{ post.author.title }} · {{ post.createdAt }}</span>
      </div>
      <el-tag v-if="post.isFeatured" type="warning" effect="light" size="small">精</el-tag>
    </div>

    <div class="post-content">
      <p>{{ post.content }}</p>

      <!-- 标签 -->
      <div class="post-tags" v-if="post.tags && post.tags.length">
        <el-tag v-for="tag in post.tags" :key="tag" type="info" size="small" effect="plain">
          # {{ tag }}
        </el-tag>
      </div>

      <!-- 图片 -->
      <div v-if="post.images && post.images.length" class="post-images">
        <el-image
          v-for="(image, i) in post.images"
          :key="i"
          :src="image"
          :preview-src-list="post.images"
          :initial-index="i"
          fit="cover"
          lazy
          hide-on-click-modal
        ></el-image>
      </div>

      <!-- 附件 -->
      <div v-if="post.attachments && post.attachments.length" class="post-attachments">
        <div v-for="(att, i) in post.attachments" :key="i" class="attachment-item">
          <el-icon><Document /></el-icon>
          <span>{{ att.name }} ({{ att.size }})</span>
          <el-tooltip content="下载附件" placement="top">
            <el-button text type="primary" size="small" icon="Download"></el-button>
          </el-tooltip>
        </div>
      </div>
    </div>

    <div class="post-actions">
      <span>
        <el-icon><Pointer /></el-icon> {{ post.likes }}
      </span>
      <span>
        <el-icon><ChatDotRound /></el-icon> {{ post.comments }}
      </span>
      <span>
        <el-icon><Star /></el-icon> {{ post.favorites }}
      </span>
      <el-button text type="primary" class="share-btn" icon="Share">分享</el-button>
    </div>
  </el-card>
</template>

<style scoped>
.post-card {
  transition: all 0.3s ease;
  border-radius: 8px;
  overflow: hidden;
  border: none;
  animation: fadeIn 0.5s ease forwards;
  width: 100%;
}

.post-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}

.post-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  gap: 10px;
  flex-wrap: wrap;
}

.author-info {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}

.author-name {
  font-weight: bold;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.post-meta {
  font-size: 12px;
  color: #999;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.post-content {
  margin-bottom: 15px;
  width: 100%;
}

.post-content p {
  line-height: 1.7;
  color: #333;
  margin-bottom: 10px;
  word-break: break-word;
}

.post-tags {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.post-tags .el-tag {
  transition: all 0.3s ease;
  margin-bottom: 4px;
}

.post-tags .el-tag:hover {
  transform: translateY(-2px);
}

.post-images {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 8px;
  margin-top: 15px;
  width: 100%;
}

.post-images .el-image {
  width: 100%;
  height: 150px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.post-images .el-image:hover {
  transform: scale(1.02);
}

.post-attachments {
  margin-top: 15px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

.attachment-item {
  display: flex;
  align-items: center;
  gap: 5px;
  background-color: #f5f7fa;
  padding: 10px 15px;
  border-radius: 8px;
  font-size: 13px;
  transition: background-color 0.3s ease;
}

.attachment-item:hover {
  background-color: #eef1f6;
}

.attachment-item .el-icon {
  color: #666;
  flex-shrink: 0;
}

.attachment-item span {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  min-width: 0;
}

.post-actions {
  display: flex;
  align-items: center;
  gap: 30px;
  color: #666;
  font-size: 14px;
  border-top: 1px solid #f0f0f0;
  padding-top: 15px;
  flex-wrap: wrap;
}

.post-actions span {
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
  transition: color 0.3s ease;
  min-width: 50px;
}

.post-actions span:hover {
  color: #409eff;
}

.share-btn {
  margin-left: auto;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (min-width: 769px) and (max-width: 1200px) {
  .post-images {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  }

  .post-images .el-image {
    height: 120px;
  }

  .post-actions {
    gap: 20px;
  }
}

@media (max-width: 768px) {
  .post-images {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  }

  .post-images .el-image {
    height: 100px;
  }

  .post-actions {
    gap: 15px;
    padding-top: 10px;
  }

  .post-actions span {
    min-width: 40px;
  }
}

@media (max-width: 480px) {
  .post-header {
    margin-bottom: 10px;
  }

  .post-content p {
    font-size: 14px;
  }

  .post-images {
    grid-template-columns: repeat(2, 1fr);
    gap: 5px;
  }

  .post-images .el-image {
    height: 90px;
  }

  .post-actions {
    gap: 10px;
    font-size: 12px;
    justify-content: space-between;
  }

  .share-btn {
    margin-left: 0;
    margin-top: 10px;
    width: 100%;
    justify-content: center;
  }
}
</style>
