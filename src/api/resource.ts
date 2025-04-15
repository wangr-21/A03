import { request } from './index';
import resourceData from '@/assets/resources.json';

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
  pdfUrl?: string;
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
const allResources: Resource[] = resourceData;

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
