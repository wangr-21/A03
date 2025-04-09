<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import type { Post } from '@/api';
import PostCard from './PostCard.vue';

const props = defineProps<{
  posts: Post[];
  loading: boolean;
  noMorePosts: boolean;
}>();

const emit = defineEmits<{
  'load-more': [];
  'remove-post': [postId: number];
}>();

// 使用本地数组来管理帖子列表，以便在取消收藏时可以立即从UI中移除帖子
const localPosts = ref<Post[]>([]);

// 监听props中的posts变化，更新本地数据
watch(
  () => props.posts,
  (newPosts) => {
    localPosts.value = [...newPosts];
  },
  { immediate: true },
);

const isEmpty = computed(() => !props.loading && localPosts.value.length === 0);

const handleLoadMore = () => {
  emit('load-more');
};

// 处理帖子移除
const handleRemovePost = (postId: number) => {
  // 从本地列表中移除帖子
  localPosts.value = localPosts.value.filter((post) => post.id !== postId);
  // 通知父组件
  emit('remove-post', postId);
};
</script>

<template>
  <div class="post-feed" v-loading="loading && localPosts.length === 0">
    <PostCard
      v-for="(post, index) in localPosts"
      :key="post.id"
      :post="post"
      :index="index"
      @remove-post="handleRemovePost"
    />

    <!-- 加载更多 / 没有更多 -->
    <div class="load-more">
      <el-button v-if="!noMorePosts" :loading="loading" @click="handleLoadMore" link>
        {{ loading ? '加载中...' : '加载更多' }}
      </el-button>
      <el-divider v-if="noMorePosts && localPosts.length > 0">没有更多了</el-divider>
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
