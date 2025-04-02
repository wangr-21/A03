import { request } from './index';

export interface Student {
  id: string;
  name: string;
  avatar?: string;
  grade: string;
  class: string;
  score: number;
  attendance: number;
}

export interface StudentsResponse {
  success: boolean;
  data: {
    students: Student[];
    total: number;
  };
}

export interface StatItem {
  label: string;
  value: string;
  icon: string;
  colorClass: string;
}

// 获取学生列表
export async function getStudents(params: {
  search?: string;
  page: number;
  pageSize: number;
}): Promise<StudentsResponse> {
  // 真实环境下应该是:
  // return request.get('/lighthouse/students', { params });

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 1000));

  const students: Student[] = [
    {
      id: '20230001',
      name: '张明',
      grade: '七年级',
      class: '1班',
      score: 92,
      attendance: 98,
      avatar: '/src/assets/avatar1.png',
    },
    {
      id: '20230002',
      name: '李华',
      grade: '七年级',
      class: '1班',
      score: 85,
      attendance: 95,
      avatar: '/src/assets/avatar2.png',
    },
    {
      id: '20230003',
      name: '王芳',
      grade: '七年级',
      class: '2班',
      score: 78,
      attendance: 90,
      avatar: '/src/assets/avatar3.png',
    },
    {
      id: '20230004',
      name: '赵强',
      grade: '七年级',
      class: '2班',
      score: 88,
      attendance: 92,
      avatar: '/src/assets/avatar4.png',
    },
    {
      id: '20230005',
      name: '刘洋',
      grade: '七年级',
      class: '3班',
      score: 76,
      attendance: 85,
      avatar: '/src/assets/avatar5.png',
    },
    {
      id: '20230006',
      name: '陈思',
      grade: '七年级',
      class: '3班',
      score: 95,
      attendance: 99,
      avatar: '/src/assets/avatar6.png',
    },
  ];

  // 筛选
  let filteredStudents = students;
  if (params.search) {
    const searchLower = params.search.toLowerCase();
    filteredStudents = students.filter(
      (student) =>
        student.name.toLowerCase().includes(searchLower) ||
        student.id.includes(params.search || ''),
    );
  }

  // 分页
  const startIndex = (params.page - 1) * params.pageSize;
  const endIndex = startIndex + params.pageSize;
  const pagedStudents = filteredStudents.slice(startIndex, endIndex);

  return {
    success: true,
    data: {
      students: pagedStudents,
      total: filteredStudents.length,
    },
  };
}

// 获取统计数据
export async function getStatistics(): Promise<StatItem[]> {
  // 真实环境下应该是:
  // return request.get('/lighthouse/statistics');

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 500));

  return [
    {
      label: '总学生数',
      value: '256',
      icon: 'User',
      colorClass: 'blue-bg',
    },
    {
      label: '平均成绩',
      value: '86.5',
      icon: 'DataLine',
      colorClass: 'green-bg',
    },
    {
      label: '出勤率',
      value: '97%',
      icon: 'Calendar',
      colorClass: 'orange-bg',
    },
    {
      label: '成长指数',
      value: '+15%',
      icon: 'TrendCharts',
      colorClass: 'purple-bg',
    },
  ];
}
