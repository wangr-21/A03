<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import {
  ElMessage,
  ElDialog,
  ElButton,
  ElInput,
  ElTabs,
  ElTabPane,
  ElCard,
  ElRow,
  ElCol,
  ElTag,
  ElAvatar,
  ElIcon,
  ElTooltip,
  ElUpload,
  ElImage,
  ElEmpty,
} from 'element-plus'
import type { UploadProps, UploadUserFile } from 'element-plus'

// 定义类型
interface Author {
  name: string
  title: string
  avatar: string
}

interface Attachment {
  name: string
  size: string
}

interface Post {
  id: number
  author: Author
  createdAt: string
  content: string
  images: string[]
  attachments: Attachment[]
  tags: string[]
  likes: number
  comments: number
  favorites: number
  isFeatured: boolean
}

interface PostForm {
  content: string
  images: UploadUserFile[]
  attachments: UploadUserFile[]
  tags: string[]
}

// --- Post Creation State ---
const showPostDialog = ref<boolean>(false)
const newPostForm = reactive<PostForm>({
  content: '',
  images: [] as UploadUserFile[],
  attachments: [] as UploadUserFile[],
  tags: [],
})
const isPosting = ref<boolean>(false)
const availableTags = ref<string[]>([
  'AI教学',
  '课堂互动',
  '教学资源',
  '项目式学习',
  '新课标',
  '德育教育',
  '家校沟通',
]) // Example tags

// --- Feed State ---
const activeTab = ref<string>('latest')
const searchQuery = ref<string>('')
const posts = ref<Post[]>([]) // Holds the list of posts
const loadingMore = ref<boolean>(false)
const noMorePosts = ref<boolean>(false)
const currentPage = ref<number>(1)
// const pageSize = ref<number>(5); // Number of posts per page

// --- Sidebar State ---
interface RecommendedUser {
  name: string
  title: string
  avatar: string
}

const recommendedUsers = ref<RecommendedUser[]>([])
const hotTags = ref<string[]>([])

// --- Placeholder Functions ---

const openPostDialog = (): void => {
  // Reset form maybe?
  newPostForm.content = ''
  newPostForm.images = []
  newPostForm.attachments = []
  newPostForm.tags = []
  showPostDialog.value = true
}

const handlePostImageUpload: UploadProps['onChange'] = (uploadFile, uploadFiles) => {
  // Limit number of images maybe?
  newPostForm.images = uploadFiles
}

const handlePostAttachmentUpload: UploadProps['onChange'] = (uploadFile, uploadFiles) => {
  newPostForm.attachments = uploadFiles
}

const submitPost = async (): Promise<void> => {
  if (!newPostForm.content.trim()) {
    ElMessage.warning('帖子内容不能为空！')
    return
  }
  isPosting.value = true
  console.log('Submitting post:', newPostForm)
  // TODO: Implement actual API call to submit post
  // This would likely involve uploading files first, then sending content + file URLs + tags
  await new Promise((resolve) => setTimeout(resolve, 1500)) // Simulate delay

  // Add the new post to the top of the feed (simulation)
  posts.value.unshift({
    id: Date.now(), // Use timestamp as temporary ID
    author: { name: '我', title: '当前用户', avatar: '/src/assets/my_avatar.jpg' }, // Replace with actual user data
    createdAt: '刚刚',
    content: newPostForm.content,
    images: newPostForm.images.map((f) => URL.createObjectURL(f.raw!)), // Create preview URLs
    attachments: newPostForm.attachments.map((f) => ({
      name: f.name,
      size: f.size ? `${(f.size / 1024).toFixed(1)}KB` : '未知',
    })),
    tags: newPostForm.tags,
    likes: 0,
    comments: 0,
    favorites: 0,
    isFeatured: false,
  })

  isPosting.value = false
  showPostDialog.value = false
  ElMessage.success('帖子发布成功！')
}

const fetchPosts = async (loadMore: boolean = false): Promise<void> => {
  if (loadingMore.value) return
  loadingMore.value = true
  console.log(
    `Fetching posts: page=${currentPage.value}, tab=${activeTab.value}, search=${searchQuery.value}`,
  )

  // Simulate API call
  await new Promise((resolve) => setTimeout(resolve, 1000))
  // Replace with actual API call, passing pagination, filter, sort parameters
  const newPosts: Post[] = [
    // Generate some dummy posts for simulation
    {
      id: 100 + currentPage.value * 5 - 4,
      author: { name: '王老师', title: '特级教师', avatar: '/src/assets/teacher1.svg' },
      createdAt: '2小时前',
      content: '分享一个关于《红楼梦》人物分析的教学设计...',
      images: [],
      attachments: [{ name: '教学设计.docx', size: '1.2MB' }],
      likes: 125,
      comments: 32,
      favorites: 58,
      isFeatured: true,
      tags: ['教学设计', '语文'],
    },
    {
      id: 100 + currentPage.value * 5 - 3,
      author: { name: '李老师', title: '骨干教师', avatar: '/src/assets/teacher2.svg' },
      createdAt: '5小时前',
      content: '推荐一个AI批改数学作业的工具... #AI助教',
      images: ['/src/assets/ai_tool.png'],
      attachments: [],
      likes: 88,
      comments: 15,
      favorites: 40,
      isFeatured: false,
      tags: ['AI教学', '数学'],
    },
    {
      id: 100 + currentPage.value * 5 - 2,
      author: { name: '张老师', title: '青年教师', avatar: '/src/assets/teacher3.svg' },
      createdAt: '昨天',
      content: '用「幻画实验室」的风格迁移功能，看看孩子们的创意大作！',
      images: ['/src/assets/artwork_styled1.jpg', '/src/assets/artwork_styled2.jpg'],
      attachments: [],
      likes: 210,
      comments: 45,
      favorites: 95,
      isFeatured: false,
      tags: ['美术', 'AI创作'],
    },
    {
      id: 100 + currentPage.value * 5 - 1,
      author: { name: '赵老师', title: '教研组长', avatar: '/src/assets/teacher4.svg' },
      createdAt: '2天前',
      content: '关于项目式学习的一些思考和实践案例分享。',
      images: [],
      attachments: [],
      likes: 150,
      comments: 28,
      favorites: 70,
      isFeatured: false,
      tags: ['项目式学习'],
    },
    {
      id: 100 + currentPage.value * 5 - 0,
      author: { name: '孙老师', title: '信息技术教师', avatar: '/src/assets/teacher5.svg' },
      createdAt: '3天前',
      content: '如何利用在线工具进行互动课堂测验？',
      images: [],
      attachments: [{ name: '工具对比.pdf', size: '800KB' }],
      likes: 95,
      comments: 12,
      favorites: 35,
      isFeatured: false,
      tags: ['课堂互动', '在线工具'],
    },
  ]

  if (loadMore) {
    posts.value = [...posts.value, ...newPosts]
  } else {
    posts.value = newPosts // Replace current posts
  }

  // Simulate end of data
  if (currentPage.value >= 3) {
    noMorePosts.value = true
  } else {
    noMorePosts.value = false
  }

  loadingMore.value = false
}

const handleLoadMore = (): void => {
  if (noMorePosts.value) return
  currentPage.value++
  fetchPosts(true)
}

const handleTabChange = (): void => {
  currentPage.value = 1 // Reset page
  noMorePosts.value = false
  posts.value = [] // Clear posts before fetching new tab data
  fetchPosts()
}

const handleSearch = (): void => {
  currentPage.value = 1
  noMorePosts.value = false
  posts.value = []
  fetchPosts()
}

const fetchSidebarData = async (): Promise<void> => {
  // Simulate API call for sidebar recommendations
  await new Promise((resolve) => setTimeout(resolve, 500))
  recommendedUsers.value = [
    { name: '赵教授', title: '教育学专家', avatar: '/src/assets/expert1.svg' },
    { name: '钱研究员', title: '课程设计顾问', avatar: '/src/assets/expert2.svg' },
    { name: '孙校长', title: '资深教育管理者', avatar: '/src/assets/expert3.svg' },
  ]
  hotTags.value = ['AI教学', '课堂互动', '教学资源', '项目式学习', '新课标', '德育教育']
}

// --- Lifecycle ---
onMounted(() => {
  fetchPosts() // Fetch initial posts
  fetchSidebarData() // Fetch sidebar data
})
</script>

<template>
  <div class="community-container">
    <el-row :gutter="20" class="responsive-row">
      <!-- 左侧主内容区域 -->
      <el-col :xs="24" :sm="24" :md="24" :lg="18" :xl="18">
        <div class="main-content">
          <!-- 发布帖子简化入口 -->
          <el-card class="post-creator-card simple">
            <div @click="openPostDialog" class="creator-placeholder">
              <el-avatar size="small" src="/src/assets/my_avatar.svg"></el-avatar>
              <span>分享您的教学经验、资源或创意...</span>
            </div>
            <div class="creator-actions simple">
              <el-button text @click="openPostDialog"
                ><el-icon><Picture /></el-icon>图片</el-button
              >
              <el-button text @click="openPostDialog"
                ><el-icon><Paperclip /></el-icon>附件</el-button
              >
              <el-button text @click="openPostDialog"
                ><el-icon><CollectionTag /></el-icon>话题</el-button
              >
            </div>
          </el-card>

          <!-- 帖子筛选/排序 -->
          <div class="feed-filters">
            <el-tabs v-model="activeTab" @tab-change="handleTabChange">
              <el-tab-pane label="最新发布" name="latest"></el-tab-pane>
              <el-tab-pane label="热门讨论" name="hot"></el-tab-pane>
              <el-tab-pane label="精华推荐" name="featured"></el-tab-pane>
            </el-tabs>
            <el-input
              placeholder="搜索帖子内容或标签"
              prefix-icon="Search"
              v-model="searchQuery"
              size="small"
              class="search-input"
              @keyup.enter="handleSearch"
              clearable
              @clear="handleSearch"
            >
              <template #append>
                <el-button icon="Search" @click="handleSearch"></el-button>
              </template>
            </el-input>
          </div>

          <!-- 帖子列表 Feed -->
          <div class="post-feed" v-loading="loadingMore && posts.length === 0">
            <el-card class="post-card" v-for="(post, index) in posts" :key="post.id">
              <div class="post-header">
                <el-avatar :size="40" :src="post.author.avatar"></el-avatar>
                <div class="author-info">
                  <span class="author-name">{{ post.author.name }}</span>
                  <span class="post-meta">{{ post.author.title }} · {{ post.createdAt }}</span>
                </div>
                <el-tag v-if="post.isFeatured" type="warning" effect="light" size="small"
                  >精</el-tag
                >
              </div>
              <div class="post-content">
                <p>{{ post.content }}</p>
                <!-- Tags -->
                <div class="post-tags" v-if="post.tags && post.tags.length">
                  <el-tag
                    v-for="tag in post.tags"
                    :key="tag"
                    type="info"
                    size="small"
                    effect="plain"
                    ># {{ tag }}</el-tag
                  >
                </div>
                <!-- Images -->
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
                <!-- Attachments -->
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
                <span
                  ><el-icon><Pointer /></el-icon> {{ post.likes }}</span
                >
                <span
                  ><el-icon><ChatDotRound /></el-icon> {{ post.comments }}</span
                >
                <span
                  ><el-icon><Star /></el-icon> {{ post.favorites }}</span
                >
                <el-button text type="primary" class="share-btn" icon="Share">分享</el-button>
              </div>
            </el-card>
            <!-- Loading More / No More -->
            <div class="load-more">
              <el-button v-if="!noMorePosts" :loading="loadingMore" @click="handleLoadMore" link>
                {{ loadingMore ? '加载中...' : '加载更多' }}
              </el-button>
              <el-divider v-if="noMorePosts && posts.length > 0">没有更多了</el-divider>
            </div>
            <el-empty
              v-if="!loadingMore && posts.length === 0"
              description="暂无相关帖子"
            ></el-empty>
          </div>
        </div>
      </el-col>

      <!-- 右侧边栏 -->
      <el-col :xs="24" :sm="24" :md="24" :lg="6" :xl="6">
        <div class="right-sidebar">
          <!-- Recommended Users Card -->
          <el-card class="recommend-card">
            <template #header>
              <div class="card-header">
                <h3>推荐合作者</h3>
                <el-button text type="primary" size="small">换一批</el-button>
              </div>
            </template>
            <div class="recommend-list">
              <div class="recommend-item" v-for="(user, index) in recommendedUsers" :key="index">
                <el-avatar :size="35" :src="user.avatar"></el-avatar>
                <div class="user-info">
                  <span class="user-name">{{ user.name }}</span>
                  <span class="user-title">{{ user.title }}</span>
                </div>
                <el-button circle icon="Plus" size="small" title="添加关注"></el-button>
              </div>
              <el-empty
                v-if="!recommendedUsers.length"
                description="暂无推荐"
                :image-size="50"
              ></el-empty>
            </div>
          </el-card>
          <!-- Hot Tags Card -->
          <el-card class="tags-card">
            <template #header>
              <div class="card-header">
                <h3>热门话题</h3>
                <el-button text type="primary" size="small">查看更多</el-button>
              </div>
            </template>
            <div class="tag-list">
              <el-tag v-for="tag in hotTags" :key="tag" class="hot-tag" effect="plain"
                ># {{ tag }}</el-tag
              >
            </div>
            <el-empty v-if="!hotTags.length" description="暂无热门话题" :image-size="50"></el-empty>
          </el-card>
        </div>
      </el-col>
    </el-row>

    <!-- Post Creation Dialog -->
    <el-dialog v-model="showPostDialog" title="发布新帖子" width="60%" top="8vh" destroy-on-close>
      <el-form :model="newPostForm" label-position="top">
        <el-form-item label="分享内容">
          <el-input
            type="textarea"
            v-model="newPostForm.content"
            :rows="5"
            placeholder="尽情分享您的想法、经验或资源..."
            resize="none"
            maxlength="2000"
            show-word-limit
          ></el-input>
        </el-form-item>
        <el-form-item label="添加图片 (可选)">
          <el-upload
            action="/api/upload-image"
            list-type="picture-card"
            v-model:file-list="newPostForm.images"
            :on-change="handlePostImageUpload"
            multiple
            accept="image/*"
            :limit="9"
          >
            <el-icon><Plus /></el-icon>
            <template #tip>
              <div class="el-upload__tip">支持 JPG、PNG 格式，单张不超过 5MB</div>
            </template>
          </el-upload>
        </el-form-item>
        <el-form-item label="添加附件 (可选)">
          <el-upload
            action="/api/upload-file"
            v-model:file-list="newPostForm.attachments"
            :on-change="handlePostAttachmentUpload"
            multiple
            :limit="5"
          >
            <el-button type="primary" plain icon="Upload">点击上传附件</el-button>
            <template #tip>
              <div class="el-upload__tip">文件大小不超过 50MB，支持各种常见文档格式</div>
            </template>
          </el-upload>
        </el-form-item>
        <el-form-item label="添加话题标签 (可选)">
          <el-select
            v-model="newPostForm.tags"
            multiple
            filterable
            allow-create
            default-first-option
            placeholder="选择或创建话题标签"
            style="width: 100%"
            :max="5"
          >
            <el-option v-for="item in availableTags" :key="item" :label="item" :value="item" />
          </el-select>
          <div class="form-tip">最多添加5个标签，每个标签不超过10个字符</div>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showPostDialog = false">取消</el-button>
          <el-button
            type="primary"
            @click="submitPost"
            :loading="isPosting"
            :disabled="!newPostForm.content.trim()"
          >
            {{ isPosting ? '发布中...' : '确认发布' }}
          </el-button>
        </span>
      </template>
    </el-dialog>
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
  .feed-filters {
    flex-direction: column;
  }
  .search-input {
    margin-top: 10px;
    width: 100%;
  }
  .right-sidebar {
    position: static;
    top: auto;
  }
}

@media (min-width: 769px) and (max-width: 1200px) {
  .post-images .el-image {
    height: 120px;
  }
}

/* 左侧主内容 */
.post-creator-card {
  margin-bottom: 20px;
  transition: all 0.3s ease;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.creator-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 15px;
}

.action-icons {
  display: flex;
  gap: 15px;
  font-size: 20px;
  color: #666;
  cursor: pointer;
}

.action-icons .el-icon:hover {
  color: #409eff;
}

.feed-filters {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  background-color: white;
  padding: 0 15px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.search-input {
  width: 250px;
}

.post-feed {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.post-card {
  transition: all 0.3s ease;
  border-radius: 8px;
  overflow: hidden;
  border: none;
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
}

.author-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.author-name {
  font-weight: bold;
  color: #333;
}

.post-meta {
  font-size: 12px;
  color: #999;
}

.post-content {
  margin-bottom: 15px;
}

.post-content p {
  line-height: 1.7;
  color: #333;
  margin-bottom: 10px;
}

.post-images {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 8px;
  margin-top: 15px;
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
}

.attachment-item span {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.post-actions {
  display: flex;
  align-items: center;
  gap: 20px;
  color: #666;
  font-size: 14px;
  border-top: 1px solid #f0f0f0;
  padding-top: 15px;
}

.post-actions span {
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
  transition: color 0.3s ease;
}

.post-actions span:hover {
  color: #409eff;
}

.share-btn {
  margin-left: auto;
}

.load-more {
  text-align: center;
  margin: 30px 0;
}

/* 右侧边栏 */
.right-sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: sticky;
  top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  font-size: 16px;
  font-weight: bold;
  margin: 0;
  color: #333;
}

.recommend-card,
.tags-card {
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
  margin-bottom: 20px;
  border: none;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.recommend-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.recommend-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.recommend-item:hover {
  background-color: #f5f7fa;
}

.user-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 500;
  font-size: 14px;
  color: #333;
}

.user-title {
  font-size: 12px;
  color: #999;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.hot-tag {
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 8px 12px;
  border-radius: 4px;
}

.hot-tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Simplified Post Creator */
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

/* Feed Filters */
.feed-filters {
  background-color: #fff;
  padding: 5px 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.feed-filters .el-tabs {
  margin-bottom: -1px; /* Align with bottom border */
}

/* Post Card adjustments */
.post-tags {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.post-tags .el-tag {
  transition: all 0.3s ease;
}
.post-tags .el-tag:hover {
  transform: translateY(-2px);
}
.post-images {
  margin-top: 15px;
}
.post-attachments {
  margin-top: 15px;
}
.attachment-item .el-button {
  margin-left: auto; /* Push download button to right */
}

/* Load More Button */
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

/* Right Sidebar */
.right-sidebar {
  position: sticky; /* Make sidebar sticky */
  top: 20px; /* Adjust based on header height */
  z-index: 1;
}
.recommend-card,
.tags-card {
  margin-bottom: 20px;
}

/* Dialog Styles */
.el-dialog__body .el-form-item {
  margin-bottom: 20px;
}
.el-dialog {
  border-radius: 8px;
  overflow: hidden;
}
.el-dialog__header {
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
}
.el-dialog__body {
  padding: 20px 30px;
}
.el-dialog__footer {
  padding: 15px 20px 20px;
  border-top: 1px solid #f0f0f0;
}
.el-upload-list--picture-card .el-upload--picture-card {
  width: 100px;
  height: 100px;
  border-radius: 8px;
  line-height: 100px;
  transition: all 0.3s ease;
}
.el-upload-list--picture-card .el-upload--picture-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
.el-upload-list--picture-card .el-upload-list__item {
  width: 100px;
  height: 100px;
  border-radius: 8px;
  margin: 0 8px 8px 0;
}

/* 交互动画 */
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

.post-card {
  animation: fadeIn 0.5s ease forwards;
}

.post-card:nth-child(1) {
  animation-delay: 0.1s;
}
.post-card:nth-child(2) {
  animation-delay: 0.2s;
}
.post-card:nth-child(3) {
  animation-delay: 0.3s;
}
.post-card:nth-child(4) {
  animation-delay: 0.4s;
}
.post-card:nth-child(5) {
  animation-delay: 0.5s;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
  line-height: 1.4;
}
</style>
