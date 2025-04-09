<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
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

const route = useRoute();
const router = useRouter();

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
const activeTag = ref<string>(''); // 当前选中的热门话题

// 处理从收藏列表中移除帖子
const handleRemovePost = (postId: number) => {
  // 从当前帖子列表中移除该帖子
  posts.value = posts.value.filter((post) => post.id !== postId);

  // 如果在移除后发现列表为空，且当前在收藏标签页，显示友好提示
  if (posts.value.length === 0 && activeTab.value === 'favorites') {
    ElMessage.info('您的收藏列表已清空，可以切换到其他标签页浏览更多内容');
  }
};

// 检查URL参数中是否有标签和标签页
const checkUrlParams = () => {
  // 检查tag参数
  if (route.query.tag) {
    activeTag.value = route.query.tag as string;
    // 重置页码并获取帖子
    currentPage.value = 1;
    noMorePosts.value = false;
    posts.value = [];
    fetchPosts();
    ElMessage.success(`正在查看"${activeTag.value}"相关的帖子`);
  }

  // 检查tab参数
  if (route.query.tab) {
    activeTab.value = route.query.tab as string;
    // 重置页码并获取帖子
    currentPage.value = 1;
    noMorePosts.value = false;
    posts.value = [];
    fetchPosts();

    if (activeTab.value === 'favorites') {
      ElMessage.success('正在查看您收藏的帖子');
    }
  }
};

// 监听路由变化，以便支持从其他页面跳转过来时带上参数
watch(
  () => route.query,
  (newQuery) => {
    // 如果URL中的标签与当前选中的标签不同，则更新
    const queryTag = newQuery.tag as string;
    if (queryTag !== activeTag.value) {
      activeTag.value = queryTag || '';
      // 重置页码并获取帖子
      currentPage.value = 1;
      noMorePosts.value = false;
      posts.value = [];
      fetchPosts();
    }

    // 如果URL中的标签页与当前标签页不同，则更新
    const queryTab = newQuery.tab as string;
    if (queryTab && queryTab !== activeTab.value) {
      activeTab.value = queryTab;
      // 重置页码并获取帖子
      currentPage.value = 1;
      noMorePosts.value = false;
      posts.value = [];
      fetchPosts();
    }
  },
);

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
    `Fetching posts: page=${currentPage.value}, tab=${activeTab.value}, search=${searchQuery.value}, tag=${activeTag.value}`,
  );

  try {
    const response = await getPosts({
      page: currentPage.value,
      tab: activeTab.value,
      search: searchQuery.value,
      tag: activeTag.value, // 添加标签筛选参数
    });

    if (loadMore) {
      posts.value = [...posts.value, ...response.data.posts];
    } else {
      posts.value = response.data.posts;
    }

    noMorePosts.value = !response.data.hasMore;

    // 如果是收藏标签页且没有帖子，显示友好提示
    if (activeTab.value === 'favorites' && posts.value.length === 0 && !loadMore) {
      ElMessage.info('您暂时没有收藏的帖子，浏览内容时点击收藏按钮添加');
    }
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

  // 更新URL参数
  router.replace({
    query: { ...route.query, tab },
  });

  if (tab === 'favorites') {
    ElMessage.success('正在查看您收藏的帖子');
  }

  // 获取新标签页的数据
  fetchPosts();
};

const handleSearch = (query: string): void => {
  searchQuery.value = query;
  currentPage.value = 1;
  noMorePosts.value = false;
  posts.value = [];
  fetchPosts();
};

// 处理热门话题标签点击
const handleTagSelected = (tag: string): void => {
  if (activeTag.value === tag) {
    // 如果点击的是已选中的标签，则取消选择
    activeTag.value = '';
    // 更新URL，移除标签参数
    router.replace({
      query: { ...route.query, tag: undefined },
    });
  } else {
    activeTag.value = tag;
    // 更新URL，添加标签参数
    router.replace({
      query: { ...route.query, tag },
    });
  }

  // 重置页码并重新获取帖子
  currentPage.value = 1;
  noMorePosts.value = false;
  posts.value = [];
  fetchPosts();

  if (tag) {
    ElMessage.success(`正在查看"${tag}"相关的帖子`);
  }
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
  checkUrlParams(); // 检查URL参数
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

          <!-- 当前选中的标签提示 -->
          <div v-if="activeTag" class="active-tag-tip">
            <el-alert type="info" :closable="false" show-icon>
              当前筛选: #{{ activeTag }}
              <el-button
                type="text"
                size="small"
                class="clear-tag-btn"
                @click="handleTagSelected('')"
              >
                清除筛选
              </el-button>
            </el-alert>
          </div>

          <!-- 帖子列表 Feed -->
          <PostList
            :posts="posts"
            :loading="loadingMore"
            :no-more-posts="noMorePosts"
            @load-more="handleLoadMore"
            @remove-post="handleRemovePost"
          />
        </div>
      </el-col>

      <!-- 右侧边栏 -->
      <el-col :xs="24" :sm="24" :md="24" :lg="6" :xl="6">
        <div class="right-sidebar">
          <!-- 推荐用户卡片 -->
          <RecommendedUsers :users="recommendedUsers" />

          <!-- 热门话题卡片 -->
          <HotTopics :tags="hotTags" :active-tag="activeTag" @tag-selected="handleTagSelected" />
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
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
}

.active-tag-tip {
  margin-bottom: 15px;
}

.clear-tag-btn {
  margin-left: 10px;
  color: var(--el-color-primary);
}

/* 响应式设计调整 */
@media (max-width: 1200px) {
  .community-container {
    padding: 15px;
  }

  .responsive-row {
    margin-left: 0 !important;
    margin-right: 0 !important;
  }
}

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
  width: 100%;
}

/* 右侧边栏 */
.right-sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: sticky;
  top: 20px;
  z-index: 1;
  width: 100%;
}

/* 确保行间距在各种屏幕尺寸下保持适当 */
.responsive-row {
  margin-bottom: 15px;
  display: flex;
  flex-wrap: wrap;
}

/* 改善小屏幕下的元素间距 */
@media (max-width: 480px) {
  .main-content {
    gap: 15px;
  }

  .right-sidebar {
    gap: 15px;
  }
}
</style>
