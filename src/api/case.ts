import { request } from './index';

// 资源类型定义
export interface CaseResource {
  type: string;
  title: string;
  url?: string;
  description?: string;
}

// 案例类型定义
export interface CaseItem {
  id: string;
  title: string;
  story_id?: string;
  main_discipline: string;
  related_disciplines: string;
  suitable_grades: string;
  content: string;
  teaching_objectives: string;
  implementation_suggestions?: string;
  resources?: CaseResource[];
  created_at: string;
}

// 故事类型定义
export interface StoryItem {
  id: string;
  title: string;
  dynasty?: string;
  period?: string;
  theme: string;
  content: string;
  moral?: string;
  reference?: string;
  created_at: string;
}

// 分类数据类型
export interface DynastyInfo {
  name: string;
  period: string;
  subdynasties: DynastyInfo[];
}

export interface ThemeCategory {
  name: string;
  subcategories: string[];
}

export interface DisciplineCategory {
  name: string;
  subcategories: string[];
}

// 请求参数类型
export interface CaseFilters {
  story_id?: string;
  main_discipline?: string;
  related_discipline?: string;
  suitable_grade?: string;
}

export interface StoryFilters {
  dynasty?: string;
  theme?: string;
  keyword?: string;
}

export interface GenerateStoryRequest {
  dynasty?: string;
  theme: string;
  keywords: string[];
}

export interface GenerateCaseRequest {
  story_id?: string;
  main_discipline: string;
  related_disciplines: string[];
  suitable_grades: string;
}

// API 函数

// 分类数据获取
export async function getDynasties(): Promise<DynastyInfo[]> {
  return await request.get('/cultural-corridor/dynasties');
}

export async function getThemes(): Promise<ThemeCategory[]> {
  return await request.get('/cultural-corridor/themes');
}

export async function getDisciplines(): Promise<DisciplineCategory[]> {
  return await request.get('/cultural-corridor/disciplines');
}

// 故事相关接口
export async function getStories(filters: StoryFilters): Promise<StoryItem[]> {
  return await request.get('/cultural-corridor/stories', { params: filters });
}

export async function getStoryDetail(storyId: string): Promise<StoryItem> {
  return await request.get(`/cultural-corridor/stories/${storyId}`);
}

export async function generateStory(data: GenerateStoryRequest): Promise<StoryItem> {
  return await request.post('/cultural-corridor/stories', data);
}

// 案例相关接口
export async function getCases(filters: CaseFilters): Promise<CaseItem[]> {
  return await request.get('/cultural-corridor/cases', { params: filters });
}

export async function getCaseDetail(caseId: string): Promise<CaseItem> {
  return await request.get(`/cultural-corridor/cases/${caseId}`);
}

export async function generateCase(data: GenerateCaseRequest): Promise<CaseItem> {
  return await request.post('/cultural-corridor/cases', data);
}

export async function getStoryCases(storyId: string): Promise<CaseItem[]> {
  return await request.get(`/cultural-corridor/stories/${storyId}/cases`);
}
