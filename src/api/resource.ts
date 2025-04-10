import { request } from './index';

// 修改Resource接口，添加pdfPath字段
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
  pdfPath?: string; // 添加PDF文件路径字段
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
// 模拟资源数据集（已移除所有高中相关资源）
const allResources: Resource[] = [
  {
    id: 1,
    title: '【人教版】七年级上册(2024秋版)美术',
    cover: '/src/assets/resource_cover/【人教版】七年级上册(2024秋版)美术电子课本封面.jpg',
    subject: '美术',
    grade: '初一',
    type: 'textbook',
    description: '人民教育出版社出版的七年级上册美术教材',
    author: '人民教育出版社',
    publishYear: 2022,
    downloadCount: 5621,
    rating: 4.8,
    pdfPath: '/src/assets/pdfs/【人教版】七年级上册(2024秋版)美术电子课本.pdf', // 添加PDF路径
  },

  // 为其他资源也添加PDF路径
  {
    id: 2,
    title: '【人教版】七年级下册(2025年新版)美术',
    cover: '/src/assets/resource_cover/【人教版】七年级下册(2025年新版)美术电子课本封面.jpg',
    subject: '美术',
    grade: '初一',
    type: 'textbook',
    description: '人民教育出版社出版的七年级下册美术教材',
    author: '人民教育出版社',
    publishYear: 2021,
    downloadCount: 3897,
    rating: 4.7,
    pdfPath: '/src/assets/pdfs/【人教版】七年级下册(2025年新版)美术电子课本.pdf',
  },
  {
    id: 3,
    title: '【人教版】八年级上册美术',
    cover: '/src/assets/resource_cover/【人教版】八年级上册美术电子课本封面.jpg',
    subject: '美术',
    grade: '初二',
    type: 'textbook',
    description: '人民教育出版社出版的八年级上册美术教材',
    author: '人民教育出版社',
    publishYear: 2021,
    downloadCount: 3897,
    rating: 4.7,
    pdfPath: '/src/assets/pdfs/【人教版】八年级上册美术电子课本.pdf',
  },
  {
    id: 4,
    title: '【人教版】八年级下册美术',
    cover: '/src/assets/resource_cover/【人教版】八年级下册美术电子课本封面.jpg',
    subject: '美术',
    grade: '初二',
    type: 'textbook',
    description: '人民教育出版社出版的八年级下册美术教材',
    author: '人民教育出版社',
    publishYear: 2021,
    downloadCount: 3897,
    rating: 4.7,
    pdfPath: '/src/assets/pdfs/【人教版】八年级下册美术电子课本.pdf',
  },
  {
    id: 5,
    title: '【人教版】九年级上册美术',
    cover: '/src/assets/resource_cover/【人教版】九年级上册美术电子课本封面.jpg',
    subject: '美术',
    grade: '初三',
    type: 'textbook',
    description: '人民教育出版社出版的九年级上册美术教材',
    author: '人民教育出版社',
    publishYear: 2021,
    downloadCount: 3897,
    rating: 4.7,
    pdfPath: '/src/assets/pdfs/【人教版】九年级上册美术电子课本.pdf',
  },
  {
    id: 6,
    title: '【人教版】九年级下册美术',
    cover: '/src/assets/resource_cover/【人教版】九年级下册美术电子课本封面.jpg',
    subject: '美术',
    grade: '初三',
    type: 'textbook',
    description: '人民教育出版社出版的九年级下册美术教材',
    author: '人民教育出版社',
    publishYear: 2021,
    downloadCount: 3897,
    rating: 4.7,
    pdfPath: '/src/assets/pdfs/【人教版】九年级下册美术电子课本.pdf',
  },
  {
    id: 7,
    title: '【人美版】七年级上册(2024秋版)美术',
    cover: '/src/assets/resource_cover/【人美版】七年级上册(2024秋版)美术电子课本封面.jpg',
    subject: '美术',
    grade: '初一',
    type: 'textbook',
    description: '人民美术出版社出版的七年级上册美术教材',
    author: '人民美术出版社',
    publishYear: 2022,
    downloadCount: 5621,
    rating: 4.8,
    pdfPath: '/src/assets/pdfs/【人美版】七年级上册(2024秋版)美术电子课本.pdf',
  },
  {
    id: 8,
    title: '【人美版】七年级下册(2025年新版)美术',
    cover: '/src/assets/resource_cover/【人美版】七年级下册(2025年新版)美术电子课本封面.jpg',
    subject: '美术',
    grade: '初一',
    type: 'textbook',
    description: '人民美术出版社出版的七年级上册美术教材',
    author: '人民美术出版社',
    publishYear: 2022,
    downloadCount: 5621,
    rating: 4.8,
    pdfPath: '/src/assets/pdfs/【人美版】七年级下册(2025年新版)美术电子课本.pdf',
  },
  {
    id: 8,
    title: '【人美版】八年级上册美术',
    cover: '/src/assets/resource_cover/【人美版】八年级上册美术电子课本封面.jpg',
    subject: '美术',
    grade: '初二',
    type: 'textbook',
    description: '人民美术出版社出版的八年级上册美术教材',
    author: '人民美术出版社',
    publishYear: 2022,
    downloadCount: 5621,
    rating: 4.8,
    pdfPath: '/src/assets/pdfs/【人美版】八年级上册美术电子课本.pdf',
  },
  {
    id: 9,
    title: '【人美版】八年级下册美术',
    cover: '/src/assets/resource_cover/【人美版】八年级下册美术电子课本封面.jpg',
    subject: '美术',
    grade: '初二',
    type: 'textbook',
    description: '人民美术出版社出版的八年级下册美术教材',
    author: '人民美术出版社',
    publishYear: 2022,
    downloadCount: 5621,
    rating: 4.8,
    pdfPath: '/src/assets/pdfs/【人美版】八年级下册美术电子课本.pdf',
  },
  {
    id: 10,
    title: '【人美版】九年级上册美术',
    cover: '/src/assets/resource_cover/【人美版】九年级上册美术电子课本封面.jpg',
    subject: '美术',
    grade: '初三',
    type: 'textbook',
    description: '人民美术出版社出版的九年级上册美术教材',
    author: '人民美术出版社',
    publishYear: 2022,
    downloadCount: 5621,
    rating: 4.8,
    pdfPath: '/src/assets/pdfs/【人美版】九年级上册美术电子课本.pdf',
  },
  {
    id: 10,
    title: '【人美版】九年级下册美术',
    cover: '/src/assets/resource_cover/【人美版】九年级下册美术电子课本封面.jpg',
    subject: '美术',
    grade: '初三',
    type: 'textbook',
    description: '人民美术出版社出版的九年级下册美术教材',
    author: '人民美术出版社',
    publishYear: 2022,
    downloadCount: 5621,
    rating: 4.8,
    pdfPath: '/src/assets/pdfs/【人美版】九年级下册美术电子课本.pdf',
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
