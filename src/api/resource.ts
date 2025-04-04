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
    cover: '/src/assets/resource_cover1.jpg',
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
    cover: '/src/assets/resource_cover2.jpg',
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
    cover: '/src/assets/resource_cover3.jpg',
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
    title: '外研社英语九年级全册',
    cover: '/src/assets/resource_cover4.jpg',
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
    cover: '/src/assets/resource_cover5.jpg',
    subject: '党建',
    grade: '通用',
    type: 'party',
    description: '中国共产党百年历程中的重要事件和人物故事',
    author: '中共党史研究室',
    publishYear: 2021,
    downloadCount: 1897,
    rating: 4.8,
  },
  {
    id: 6,
    title: '物理实验精选（高中）',
    cover: '/src/assets/resource_cover6.jpg',
    subject: '物理',
    grade: '高中',
    type: 'textbook',
    description: '高中物理关键实验解析与操作指南',
    author: '教育科学出版社',
    publishYear: 2019,
    downloadCount: 3245,
    rating: 4.7,
  },
  {
    id: 7,
    title: '化学反应原理探究',
    cover: '/src/assets/resource_cover7.jpg',
    subject: '化学',
    grade: '高中',
    type: 'textbook',
    description: '高中化学反应原理深度解析与习题详解',
    author: '科学出版社',
    publishYear: 2021,
    downloadCount: 2786,
    rating: 4.5,
  },
  {
    id: 8,
    title: '中国近代史纲要解读',
    cover: '/src/assets/resource_cover8.jpg',
    subject: '党建',
    grade: '通用',
    type: 'party',
    description: '中国近代史重要事件与历史进程分析',
    author: '高等教育出版社',
    publishYear: 2020,
    downloadCount: 1542,
    rating: 4.6,
  },
  {
    id: 9,
    title: '生物进化论浅析',
    cover: '/src/assets/resource_cover9.jpg',
    subject: '生物',
    grade: '高中',
    type: 'textbook',
    description: '达尔文进化论与现代生物进化理论解读',
    author: '生物科学出版社',
    publishYear: 2018,
    downloadCount: 2341,
    rating: 4.4,
  },
  {
    id: 10,
    title: '小学数学思维训练',
    cover: '/src/assets/resource_cover10.jpg',
    subject: '数学',
    grade: '小学',
    type: 'material',
    description: '小学数学思维能力培养与解题技巧',
    author: '儿童教育研究所',
    publishYear: 2022,
    downloadCount: 6782,
    rating: 4.9,
  },
  {
    id: 11,
    title: '初中语文古诗文鉴赏',
    cover: '/src/assets/resource_cover11.jpg',
    subject: '语文',
    grade: '初中',
    type: 'material',
    description: '初中语文古诗文赏析与写作指导',
    author: '语文教育研究院',
    publishYear: 2021,
    downloadCount: 5421,
    rating: 4.7,
  },
  {
    id: 12,
    title: '高中历史重点事件梳理',
    cover: '/src/assets/resource_cover12.jpg',
    subject: '历史',
    grade: '高中',
    type: 'material',
    description: '中国古代、近代及世界史关键事件与线索',
    author: '历史研究出版社',
    publishYear: 2022,
    downloadCount: 3875,
    rating: 4.8,
  },
  {
    id: 13,
    title: '中学地理知识地图',
    cover: '/src/assets/resource_cover13.jpg',
    subject: '地理',
    grade: '初中',
    type: 'material',
    description: '初中地理知识结构可视化与要点归纳',
    author: '地理教育研究所',
    publishYear: 2020,
    downloadCount: 4231,
    rating: 4.6,
  },
  {
    id: 14,
    title: '高中政治思想方法论',
    cover: '/src/assets/resource_cover14.jpg',
    subject: '政治',
    grade: '高中',
    type: 'material',
    description: '高中政治辩证思维与论证方法训练',
    author: '思想教育出版社',
    publishYear: 2021,
    downloadCount: 2865,
    rating: 4.5,
  },
  {
    id: 15,
    title: '党的二十大精神解读',
    cover: '/src/assets/resource_cover15.jpg',
    subject: '党建',
    grade: '通用',
    type: 'party',
    description: '党的二十大报告要点与精神解读材料',
    author: '中央文献出版社',
    publishYear: 2022,
    downloadCount: 7865,
    rating: 4.9,
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
