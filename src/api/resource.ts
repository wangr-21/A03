import { request } from './index';

export interface Resource {
  id: number;
  title: string;
  cover: string;
  subject: string;
  grade: string;
  type: string;
}

export interface ResourcesResponse {
  success: boolean;
  data: {
    resources: Resource[];
    total: number;
  };
}

export interface ResourceFilters {
  type?: string;
  subject?: string;
  grade?: string;
  page?: number;
  pageSize?: number;
}

// 获取资源列表
export async function getResources(filters: ResourceFilters = {}): Promise<ResourcesResponse> {
  // 真实环境下应该是:
  // return request.get('/resources', { params: filters });

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 1000));

  const resources: Resource[] = [
    {
      id: 1,
      title: '人教版语文七年级上册',
      cover: '/src/assets/resource_cover1.jpg',
      subject: '语文',
      grade: '初一',
      type: 'textbook',
    },
    {
      id: 2,
      title: '北师大版数学八年级下册',
      cover: '/src/assets/resource_cover2.jpg',
      subject: '数学',
      grade: '初二',
      type: 'textbook',
    },
    {
      id: 3,
      title: '《共产党宣言》导读',
      cover: '/src/assets/resource_cover3.jpg',
      subject: '党建',
      grade: '通用',
      type: 'party',
    },
    {
      id: 4,
      title: '外研社英语九年级全册',
      cover: '/src/assets/resource_cover4.jpg',
      subject: '英语',
      grade: '初三',
      type: 'textbook',
    },
    {
      id: 5,
      title: '党史故事100讲',
      cover: '/src/assets/resource_cover5.jpg',
      subject: '党建',
      grade: '通用',
      type: 'party',
    },
    {
      id: 6,
      title: '物理实验精选（高中）',
      cover: '/src/assets/resource_cover6.jpg',
      subject: '物理',
      grade: '高中',
      type: 'textbook',
    },
    {
      id: 7,
      title: '化学反应原理探究',
      cover: '/src/assets/resource_cover7.jpg',
      subject: '化学',
      grade: '高中',
      type: 'textbook',
    },
    {
      id: 8,
      title: '中国近代史纲要解读',
      cover: '/src/assets/resource_cover8.jpg',
      subject: '党建',
      grade: '通用',
      type: 'party',
    },
    {
      id: 9,
      title: '生物进化论浅析',
      cover: '/src/assets/resource_cover9.jpg',
      subject: '生物',
      grade: '高中',
      type: 'textbook',
    },
  ];

  return {
    success: true,
    data: {
      resources,
      total: resources.length,
    },
  };
}
