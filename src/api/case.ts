import { request } from './index';

export interface CaseFilters {
  category: string;
  era: string;
  theme: string;
  page?: number;
  pageSize?: number;
}

export interface CaseItem {
  id: number;
  title: string;
  category: string;
  era: string;
  theme: string;
  summary: string;
}

export interface CasesResponse {
  success: boolean;
  data: {
    cases: CaseItem[];
    total: number;
  };
}

export interface SimulationScenario {
  title: string;
  description: string;
}

// 获取案例列表
export async function getCases(filters: CaseFilters): Promise<CasesResponse> {
  // 真实环境下应该是:
  // return request.get('/cultural-corridor/cases', { params: filters });

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 1000));

  const cases: CaseItem[] = [
    {
      id: 1,
      title: '刻舟求剑',
      category: '传统故事',
      era: '先秦',
      theme: '哲学思辨',
      summary: '...',
    },
    {
      id: 2,
      title: '《九章算术》中的勾股定理',
      category: '跨学科案例',
      era: '秦汉',
      theme: '科学探索',
      summary: '...',
    },
  ];

  return {
    success: true,
    data: {
      cases,
      total: 2,
    },
  };
}

// 获取情景模拟
export async function getSimulationScenario(type: string): Promise<SimulationScenario> {
  // 真实环境下应该是:
  // return request.get(`/cultural-corridor/scenario/${type}`);

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 500));

  return {
    title: '古诗创作场景模拟',
    description: '你身处盛唐长安，请根据以下情景创作一首七言绝句...',
  };
}
