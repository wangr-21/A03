import { request } from './index';
import questionsData from '../assets/demo/question/select.json';

export interface QuestionFilters {
  type: string[];
  difficulty: string;
  knowledgePoint: string;
  page?: number;
  pageSize?: number;
  subject?: string;
  searchTerm?: string;
}

export interface Question {
  id: number;
  type: string;
  difficulty: string;
  point: string;
  stem: string;
  answer: string;
  options?: string[];
  explanation?: string;
  subject?: string;
  grade?: string;
}

export interface QuestionsResponse {
  success: boolean;
  data: {
    questions: Question[];
    total: number;
  };
}

// 使用JSON文件中的题库数据
const allQuestions: Question[] = questionsData;

// 从题库数据中提取知识点
export const KNOWLEDGE_POINTS = Array.from(new Set(allQuestions.map((q) => q.point))).sort();

// 从题库数据中提取题目类型
export const QUESTION_TYPES = Array.from(new Set(allQuestions.map((q) => q.type))).sort();

// 从题库数据中提取难度级别
export const DIFFICULTY_LEVELS = Array.from(new Set(allQuestions.map((q) => q.difficulty))).sort();

// 从题库数据中提取学科
export const SUBJECTS = Array.from(
  new Set(allQuestions.map((q) => q.subject).filter(Boolean)),
).sort();

// 获取题目列表
export async function getQuestions(filters: QuestionFilters): Promise<QuestionsResponse> {
  // 模拟API调用延迟
  await new Promise((resolve) => setTimeout(resolve, 800));

  // 筛选题目
  let filteredQuestions = [...allQuestions];

  // 按题型筛选
  if (filters.type && filters.type.length > 0) {
    filteredQuestions = filteredQuestions.filter((q) => filters.type.includes(q.type));
  }

  // 按难度筛选
  if (filters.difficulty && filters.difficulty !== 'all') {
    filteredQuestions = filteredQuestions.filter((q) => q.difficulty === filters.difficulty);
  }

  // 按知识点筛选
  if (filters.knowledgePoint && filters.knowledgePoint !== 'all') {
    filteredQuestions = filteredQuestions.filter((q) => q.point === filters.knowledgePoint);
  }

  // 按学科筛选
  if (filters.subject && filters.subject !== 'all') {
    filteredQuestions = filteredQuestions.filter((q) => q.subject === filters.subject);
  }

  // 关键词搜索
  if (filters.searchTerm) {
    const keyword = filters.searchTerm.toLowerCase();
    filteredQuestions = filteredQuestions.filter(
      (q) =>
        q.stem.toLowerCase().includes(keyword) ||
        q.point.toLowerCase().includes(keyword) ||
        (q.explanation && q.explanation.toLowerCase().includes(keyword)),
    );
  }

  // 分页
  const page = filters.page || 1;
  const pageSize = filters.pageSize || 10;
  const startIndex = (page - 1) * pageSize;
  const endIndex = startIndex + pageSize;
  const paginatedQuestions = filteredQuestions.slice(startIndex, endIndex);

  return {
    success: true,
    data: {
      questions: paginatedQuestions,
      total: filteredQuestions.length,
    },
  };
}

// 获取题目详情
export async function getQuestionDetail(
  id: number,
): Promise<{ success: boolean; data: Question | null }> {
  // 模拟API调用延迟
  await new Promise((resolve) => setTimeout(resolve, 500));

  const question = allQuestions.find((q) => q.id === id) || null;

  return {
    success: !!question,
    data: question,
  };
}
