<script setup lang="ts">
import { computed } from 'vue';
import type { Post } from '@/api';
import PostCard from './PostCard.vue';

const props = defineProps<{
  posts: Post[];
  loading: boolean;
  noMorePosts: boolean;
}>();

const emit = defineEmits(['load-more']);

const isEmpty = computed(() => !props.loading && props.posts.length === 0);

const handleLoadMore = () => {
  emit('load-more');
};
</script>

<template>
  <div class="post-feed" v-loading="loading && posts.length === 0">
    <PostCard v-for="(post, index) in posts" :key="post.id" :post="post" :index="index" />

    <!-- 加载更多 / 没有更多 -->
    <div class="load-more">
      <el-button v-if="!noMorePosts" :loading="loading" @click="handleLoadMore" link>
        {{ loading ? '加载中...' : '加载更多' }}
      </el-button>
      <el-divider v-if="noMorePosts && posts.length > 0">没有更多了</el-divider>
    </div>

    <el-empty v-if="isEmpty" description="暂无相关帖子"></el-empty>
  </div>
</template>

<style scoped>
.post-feed {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.load-more {
  text-align: center;
  margin: 30px 0;
}

.load-more .el-button {
  font-size: 14px;
  padding: 10px 20px;
  transition: all 0.3s ease;
}

.load-more .el-button:hover {
  transform: translateY(-2px);
}

.load-more .el-divider {
  margin: 20px 0;
  font-size: 14px;
  color: #ccc;
}
</style>
