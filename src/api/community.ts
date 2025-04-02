import { request } from './index';
import type { UploadUserFile } from 'element-plus';

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
}

export interface PostForm {
  content: string;
  images: UploadUserFile[];
  attachments: UploadUserFile[];
  tags: string[];
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

// 获取帖子列表
export async function getPosts(params: {
  page: number;
  tab: string;
  search?: string;
}): Promise<PostsResponse> {
  // 真实环境下应该是:
  // return request.get('/community/posts', { params });

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 1000));

  const { page } = params;
  const hasMore = page < 3;

  const posts: Post[] = [
    {
      id: 100 + page * 5 - 4,
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
      id: 100 + page * 5 - 3,
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
      id: 100 + page * 5 - 2,
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
      id: 100 + page * 5 - 1,
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
      id: 100 + page * 5,
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
  ];

  return {
    success: true,
    data: {
      posts,
      total: hasMore ? 15 : 10,
      hasMore,
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
      { name: '赵教授', title: '教育学专家', avatar: '/src/assets/expert1.svg' },
      { name: '钱研究员', title: '课程设计顾问', avatar: '/src/assets/expert2.svg' },
      { name: '孙校长', title: '资深教育管理者', avatar: '/src/assets/expert3.svg' },
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
