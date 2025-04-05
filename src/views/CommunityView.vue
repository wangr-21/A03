<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { getPosts, getSidebarData, submitPost } from '@/api';
import type { Post, PostForm, RecommendedUser } from '@/api';
import {
  PostCreationEntry,
  PostCreationDialog,
  FeedHeader,
  PostList,
  RecommendedUsers,
  HotTopics,
} from '@/components/community';

// --- Post Creation State ---
const showPostDialog = ref<boolean>(false);
const isPosting = ref<boolean>(false);
const availableTags = ref<string[]>([
  'AI教学',
  '课堂互动',
  '教学资源',
  '项目式学习',
  '新课标',
  '德育教育',
  '家校沟通',
]);

// --- Feed State ---
const activeTab = ref<string>('latest');
const searchQuery = ref<string>('');
const posts = ref<Post[]>([]);
const loadingMore = ref<boolean>(false);
const noMorePosts = ref<boolean>(false);
const currentPage = ref<number>(1);

// --- Sidebar State ---
const recommendedUsers = ref<RecommendedUser[]>([]);
const hotTags = ref<string[]>([]);

// --- Functions ---
const openPostDialog = (): void => {
  showPostDialog.value = true;
};

const handleSubmitPost = async (postForm: PostForm): Promise<void> => {
  if (!postForm.content.trim()) {
    ElMessage.warning('帖子内容不能为空！');
    return;
  }

  isPosting.value = true;
  console.log('Submitting post:', postForm);

  try {
    const response = await submitPost(postForm);
    if (response.success) {
      await fetchPosts(); // 刷新列表
      showPostDialog.value = false;
      ElMessage.success('帖子发布成功！');
    } else {
      throw new Error('Failed to submit post');
    }
  } catch (error) {
    console.error('Error submitting post:', error);
    ElMessage.error('发布失败，请稍后重试');
  } finally {
    isPosting.value = false;
  }
};

const fetchPosts = async (loadMore: boolean = false): Promise<void> => {
  if (loadingMore.value) return;
  loadingMore.value = true;
  console.log(
    `Fetching posts: page=${currentPage.value}, tab=${activeTab.value}, search=${searchQuery.value}`,
  );

  try {
    const response = await getPosts({
      page: currentPage.value,
      tab: activeTab.value,
      search: searchQuery.value,
    });

    if (loadMore) {
      posts.value = [...posts.value, ...response.data.posts];
    } else {
      posts.value = response.data.posts;
    }

    noMorePosts.value = !response.data.hasMore;
  } catch (error) {
    console.error('Error fetching posts:', error);
    ElMessage.error('获取帖子失败，请稍后重试');
  } finally {
    loadingMore.value = false;
  }
};

const handleLoadMore = (): void => {
  if (noMorePosts.value) return;
  currentPage.value++;
  fetchPosts(true);
};

const handleTabChange = (tab: string): void => {
  activeTab.value = tab;
  currentPage.value = 1; // Reset page
  noMorePosts.value = false;
  posts.value = []; // Clear posts before fetching new tab data
  fetchPosts();
};

const handleSearch = (query: string): void => {
  searchQuery.value = query;
  currentPage.value = 1;
  noMorePosts.value = false;
  posts.value = [];
  fetchPosts();
};

const fetchSidebarData = async (): Promise<void> => {
  try {
    const data = await getSidebarData();
    recommendedUsers.value = data.recommendedUsers;
    hotTags.value = data.hotTags;
  } catch (error) {
    console.error('Error fetching sidebar data:', error);
    ElMessage.error('获取推荐数据失败');
  }
};

// --- Lifecycle ---
onMounted(() => {
  fetchPosts(); // Fetch initial posts
  fetchSidebarData(); // Fetch sidebar data
});
</script>

<template>
  <div class="community-container">
    <el-row :gutter="20" class="responsive-row">
      <!-- 左侧主内容区域 -->
      <el-col :xs="24" :sm="24" :md="24" :lg="18" :xl="18">
        <div class="main-content">
          <!-- 发布帖子简化入口 -->
          <PostCreationEntry @open-dialog="openPostDialog" />

          <!-- 帖子筛选/排序 -->
          <FeedHeader
            :active-tab="activeTab"
            :search-query="searchQuery"
            @tab-change="handleTabChange"
            @search="handleSearch"
          />

          <!-- 帖子列表 Feed -->
          <PostList
            :posts="posts"
            :loading="loadingMore"
            :no-more-posts="noMorePosts"
            @load-more="handleLoadMore"
          />
        </div>
      </el-col>

      <!-- 右侧边栏 -->
      <el-col :xs="24" :sm="24" :md="24" :lg="6" :xl="6">
        <div class="right-sidebar">
          <!-- 推荐用户卡片 -->
          <RecommendedUsers :users="recommendedUsers" />

          <!-- 热门话题卡片 -->
          <HotTopics :tags="hotTags" />
        </div>
      </el-col>
    </el-row>

    <!-- 帖子创建对话框 -->
    <PostCreationDialog
      v-model:visible="showPostDialog"
      :is-posting="isPosting"
      :available-tags="availableTags"
      @submit-post="handleSubmitPost"
    />
  </div>
</template>

<style scoped>
.community-container {
  padding: 20px;
}

/* 响应式设计调整 */
@media (max-width: 768px) {
  .community-container {
    padding: 10px;
  }

  .responsive-row .el-col {
    margin-bottom: 20px;
  }

  .right-sidebar {
    position: static;
    top: auto;
  }
}

/* 主内容区域 */
.main-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 右侧边栏 */
.right-sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: sticky;
  top: 20px;
  z-index: 1;
}
</style>
