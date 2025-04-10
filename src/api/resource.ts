import { request } from './index';

export interface Resource {
  id: number;
  title: string;
  cover: string;
  subject: string;
  grade: string;
  type: string;
  description?: string;
  author?: string;
  publishYear?: number;
  downloadCount?: number;
  rating?: number;
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
  keyword?: string;
}

// 模拟资源数据集
const allResources: Resource[] = [
  {
    id: 1,
    title: '人教版语文七年级上册',
    cover: '/src/assets/images/resource_cover/1.png',
    subject: '语文',
    grade: '初一',
    type: 'textbook',
    description: '人民教育出版社出版的七年级语文教材，包含古诗文、现代文阅读等内容',
    author: '人教社编写组',
    publishYear: 2022,
    downloadCount: 5621,
    rating: 4.8,
  },
  {
    id: 2,
    title: '北师大版数学八年级下册',
    cover: '/src/assets/images/resource_cover/2.png',
    subject: '数学',
    grade: '初二',
    type: 'textbook',
    description: '北京师范大学出版社出版的八年级数学教材，涵盖代数、几何等内容',
    author: '北师大编写组',
    publishYear: 2021,
    downloadCount: 3897,
    rating: 4.7,
  },
  {
    id: 3,
    title: '《共产党宣言》导读',
    cover: '/src/assets/images/resource_cover/3.png',
    subject: '党建',
    grade: '通用',
    type: 'party',
    description: '《共产党宣言》重点内容解读与思想分析',
    author: '中国社会科学院',
    publishYear: 2020,
    downloadCount: 2145,
    rating: 4.9,
  },
  {
    id: 4,
    title: '外研社英语九年级上册',
    cover: '/src/assets/images/resource_cover/4.png',
    subject: '英语',
    grade: '初三',
    type: 'textbook',
    description: '外语教学与研究出版社出版的九年级英语教材，注重听说读写全面发展',
    author: '外研社编写组',
    publishYear: 2022,
    downloadCount: 4562,
    rating: 4.6,
  },
  {
    id: 5,
    title: '党史故事100讲',
    cover: '/src/assets/images/resource_cover/5.png',
    subject: '党建',
    grade: '通用',
    type: 'party',
    description: '中国共产党百年历程中的重要事件和人物故事',
    author: '中共党史研究室',
    publishYear: 2021,
    downloadCount: 1897,
    rating: 4.8,
  },
];

// 获取资源列表
export async function getResources(filters: ResourceFilters = {}): Promise<ResourcesResponse> {
  // 真实环境下应该是:
  // return request.get('/resources', { params: filters });

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 800)); // 减少等待时间，便于开发

  // 根据过滤条件筛选资源
  let filteredResources = [...allResources];

  // 按类型筛选
  if (filters.type && filters.type !== 'all') {
    filteredResources = filteredResources.filter((resource) => resource.type === filters.type);
  }

  // 按学科筛选
  if (filters.subject) {
    filteredResources = filteredResources.filter(
      (resource) => resource.subject === filters.subject,
    );
  }

  // 按年级筛选
  if (filters.grade) {
    filteredResources = filteredResources.filter((resource) => resource.grade === filters.grade);
  }

  // 按关键词搜索（标题、描述）
  if (filters.keyword) {
    const keyword = filters.keyword.toLowerCase();
    filteredResources = filteredResources.filter(
      (resource) =>
        resource.title.toLowerCase().includes(keyword) ||
        (resource.description && resource.description.toLowerCase().includes(keyword)),
    );
  }

  // 实现分页
  const page = filters.page || 1;
  const pageSize = filters.pageSize || 10;
  const startIndex = (page - 1) * pageSize;
  const endIndex = startIndex + pageSize;
  const paginatedResources = filteredResources.slice(startIndex, endIndex);

  return {
    success: true,
    data: {
      resources: paginatedResources,
      total: filteredResources.length,
    },
  };
}

// 获取资源详情
export async function getResourceDetail(
  id: number,
): Promise<{ success: boolean; data: Resource | null }> {
  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 500));

  const resource = allResources.find((item) => item.id === id) || null;

  return {
    success: !!resource,
    data: resource,
  };
}
