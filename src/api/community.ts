import { request } from './index';
import type { UploadUserFile } from 'element-plus';
import * as avatars from '@/assets/avatars';

export interface Author {
  name: string;
  title: string;
  avatar: string;
}

export interface Attachment {
  name: string;
  size: string;
}

export interface Post {
  id: number;
  author: Author;
  createdAt: string;
  content: string;
  images: string[];
  attachments: Attachment[];
  tags: string[];
  likes: number;
  comments: number;
  favorites: number;
  isFeatured: boolean;
  isFavorited: boolean;
}

export interface PostForm {
  title: string;
  content: string;
  type: string;
  images: UploadUserFile[];
  attachments: UploadUserFile[];
  tags: string[];
  mentionedUsers: string[];
}

export interface RecommendedUser {
  name: string;
  title: string;
  avatar: string;
}

export interface PostsResponse {
  success: boolean;
  data: {
    posts: Post[];
    total: number;
    hasMore: boolean;
  };
}

// 模拟数据存储，用于模拟服务器端状态
const postFavoriteCache = new Map<number, number>();
// 模拟收藏状态的存储
const postFavoritedStatus = new Map<number, boolean>();

// 初始化或获取帖子收藏状态
export function getSyncedFavoriteStatus(postId: number, defaultStatus: boolean): boolean {
  // 如果存储中已有该帖子的收藏状态，则返回存储的状态
  if (postFavoritedStatus.has(postId)) {
    return postFavoritedStatus.get(postId) as boolean;
  }

  // 否则初始化存储，并返回默认状态
  postFavoritedStatus.set(postId, defaultStatus);
  return defaultStatus;
}

// 获取帖子列表
export async function getPosts(params: {
  page: number;
  tab: string;
  search?: string;
  tag?: string;
}): Promise<PostsResponse> {
  // 真实环境下应该是:
  // return request.get('/community/posts', { params });

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 500));

  const { page, tag, tab } = params;
  const hasMore = page < 3;

  // 基础帖子数据
  let posts: Post[] = [
    {
      id: 100 + page * 5 - 4,
      author: { name: '王老师', title: '特级教师', avatar: avatars.teacher1 },
      createdAt: '2小时前',
      content: '分享一个关于《红楼梦》人物分析的教学设计...',
      images: [],
      attachments: [{ name: '教学设计.docx', size: '1.2MB' }],
      likes: 125,
      comments: 32,
      favorites: 58,
      isFeatured: true,
      tags: ['教学设计', '语文'],
      isFavorited: true,
    },
    {
      id: 100 + page * 5 - 3,
      author: { name: '李老师', title: '骨干教师', avatar: avatars.teacher2 },
      createdAt: '5小时前',
      content: '推荐一个AI批改数学作业的工具... #AI助教',
      images: ['/src/assets/ai_tool.png'],
      attachments: [],
      likes: 88,
      comments: 15,
      favorites: 40,
      isFeatured: false,
      tags: ['AI教学', '数学'],
      isFavorited: false,
    },
    {
      id: 100 + page * 5 - 2,
      author: { name: '张老师', title: '青年教师', avatar: avatars.teacher3 },
      createdAt: '昨天',
      content: '用「幻画实验室」的风格迁移功能，看看孩子们的创意大作！',
      images: ['/src/assets/artwork_styled1.jpg', '/src/assets/artwork_styled2.jpg'],
      attachments: [],
      likes: 210,
      comments: 45,
      favorites: 95,
      isFeatured: false,
      tags: ['美术', 'AI创作'],
      isFavorited: true,
    },
    {
      id: 100 + page * 5 - 1,
      author: { name: '赵老师', title: '教研组长', avatar: avatars.teacher4 },
      createdAt: '2天前',
      content: '关于项目式学习的一些思考和实践案例分享。',
      images: [],
      attachments: [],
      likes: 150,
      comments: 28,
      favorites: 70,
      isFeatured: false,
      tags: ['项目式学习'],
      isFavorited: false,
    },
    {
      id: 100 + page * 5,
      author: {
        name: '孙老师',
        title: '信息技术教师',
        avatar: avatars.teacher5,
      },
      createdAt: '3天前',
      content: '如何利用在线工具进行互动课堂测验？',
      images: [],
      attachments: [{ name: '工具对比.pdf', size: '800KB' }],
      likes: 95,
      comments: 12,
      favorites: 35,
      isFeatured: false,
      tags: ['课堂互动', '在线工具'],
      isFavorited: false,
    },
  ];

  // 更新帖子的收藏数据，与缓存同步
  posts = posts.map((post) => {
    // 使用全局状态同步收藏状态
    post.isFavorited = getSyncedFavoriteStatus(post.id, post.isFavorited);

    // 如果缓存中有该帖子的收藏数，则使用缓存中的数据
    if (postFavoriteCache.has(post.id)) {
      post.favorites = postFavoriteCache.get(post.id) || post.favorites;
    } else {
      // 否则初始化缓存
      postFavoriteCache.set(post.id, post.favorites);
    }
    return post;
  });

  // 如果指定了标签，过滤出包含该标签的帖子
  if (tag) {
    posts = posts.filter((post) => post.tags.includes(tag));
  }

  // 如果是"我的收藏"标签，仅显示收藏的帖子
  if (tab === 'favorites') {
    posts = posts.filter((post) => post.isFavorited);
  }

  return {
    success: true,
    data: {
      posts,
      total: hasMore ? 15 : 10,
      hasMore: hasMore && posts.length > 0,
    },
  };
}

// 获取侧边栏数据
export async function getSidebarData(): Promise<{
  recommendedUsers: RecommendedUser[];
  hotTags: string[];
}> {
  // 真实环境下应该是:
  // return request.get('/community/sidebar');

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 500));

  return {
    recommendedUsers: [
      { name: '赵教授', title: '教育学专家', avatar: avatars.expert1 },
      { name: '钱研究员', title: '课程设计顾问', avatar: avatars.expert2 },
      { name: '孙校长', title: '资深教育管理者', avatar: avatars.expert3 },
    ],
    hotTags: ['AI教学', '课堂互动', '教学资源', '项目式学习', '新课标', '德育教育'],
  };
}

// 发布帖子
export async function submitPost(postForm: PostForm): Promise<{
  success: boolean;
  data: {
    postId: number;
  };
}> {
  // 真实环境下应该是:
  // 先上传文件，获取URL
  // const formData = new FormData();
  // postForm.images.forEach(file => {
  //   formData.append('images', file.raw as File);
  // });
  // postForm.attachments.forEach(file => {
  //   formData.append('attachments', file.raw as File);
  // });
  // const uploadResult = await request.post('/upload', formData);

  // 然后提交帖子
  // return request.post('/community/posts', {
  //   content: postForm.content,
  //   imageUrls: uploadResult.imageUrls,
  //   attachmentUrls: uploadResult.attachmentUrls,
  //   tags: postForm.tags
  // });

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 1500));

  return {
    success: true,
    data: {
      postId: Date.now(),
    },
  };
}

// 收藏/取消收藏帖子
export async function togglePostFavorite(
  postId: number,
  isFavorited: boolean,
): Promise<{
  success: boolean;
  data: {
    isFavorited: boolean;
    favorites: number;
  };
}> {
  // 真实环境下应该是:
  // return request.post('/community/posts/favorite', { postId, isFavorited });

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 500));

  // 如果缓存中没有该帖子的收藏数，初始化一个(20-60之间随机值)
  if (!postFavoriteCache.has(postId)) {
    const initialCount = Math.floor(Math.random() * 40) + 20;
    postFavoriteCache.set(postId, initialCount);
  }

  // 获取当前收藏数
  let currentFavorites = postFavoriteCache.get(postId) || 0;

  // 计算新的收藏数
  if (isFavorited) {
    // 如果是收藏操作，增加1
    currentFavorites += 1;
  } else {
    // 如果是取消收藏操作，减少1
    currentFavorites = Math.max(0, currentFavorites - 1);
  }

  // 更新缓存
  postFavoriteCache.set(postId, currentFavorites);

  // 更新收藏状态
  postFavoritedStatus.set(postId, isFavorited);

  return {
    success: true,
    data: {
      isFavorited: isFavorited,
      favorites: currentFavorites,
    },
  };
}

// 获取收藏的帖子
export async function getFavoritedPosts(params: { page: number }): Promise<PostsResponse> {
  // 真实环境下应该是:
  // return request.get('/community/posts/favorited', { params });

  // 这里复用getPosts，并设置tab为favorites
  return getPosts({
    page: params.page,
    tab: 'favorites',
  });
}
