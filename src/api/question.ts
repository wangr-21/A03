import { request } from './index';

export interface QuestionFilters {
  type: string[];
  difficulty: string;
  knowledgePoint: string;
  page?: number;
  pageSize?: number;
}

export interface Question {
  id: number;
  type: string;
  difficulty: string;
  point: string;
  stem: string;
  answer: string;
}

export interface QuestionsResponse {
  success: boolean;
  data: {
    questions: Question[];
    total: number;
  };
}

// 获取题目列表
export async function getQuestions(filters: QuestionFilters): Promise<QuestionsResponse> {
  // 真实环境下应该是:
  // return request.get('/question-bank/questions', { params: filters });

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 1000));

  const questions: Question[] = [
    {
      id: 1,
      type: '选择题',
      difficulty: 'easy',
      point: '函数',
      stem: '下列哪个是函数 y = 2x + 1 的图像？',
      answer: 'A',
    },
    {
      id: 2,
      type: '填空题',
      difficulty: 'medium',
      point: '几何',
      stem: '三角形内角和是____度。',
      answer: '180',
    },
  ];

  return {
    success: true,
    data: {
      questions,
      total: 2,
    },
  };
}
