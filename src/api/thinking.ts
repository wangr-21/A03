import { request } from './index';

// 活动步骤
interface ActivityStep {
  name: string;
  duration: number;
  teacher_action: string;
  student_action: string;
}

// 活动评价
interface ActivityEvaluation {
  criteria: string[];
  method: string;
}

// 互动教学活动
export interface Activity {
  // metadata
  id: string;
  activity_type: string;
  subject: string;
  grade: string;
  duration: number;
  created_at: string;

  // content
  title: string;
  description: string;
  preparation: string[];
  objectives: string[];
  steps: ActivityStep[];
  evaluation: ActivityEvaluation;
  extensions: string[];
}

// 场景组件
interface ScenarioScene {
  name: string;
  description: string;
  visual_elements: string[];
  audio_elements: string[];
}

interface ScenarioCharacter {
  name: string;
  role: string;
  description: string;
}

interface ScenarioInteractiveElement {
  type: string;
  description: string;
  options: string[];
  outcomes: string[];
}

interface ScenarioTeacherGuide {
  setup: string[];
  facilitation_tips: string[];
  reflection_questions: string[];
}

// 情景模拟场景
export interface Scenario {
  // metadata
  id: string;
  scenario_type: string;
  subject: string;
  grade: string;
  created_at: string;

  // content
  title: string;
  background: string;
  educational_value: string;
  scenes: ScenarioScene[];
  characters: ScenarioCharacter[];
  interactive_elements: ScenarioInteractiveElement[];
  teacher_guide: ScenarioTeacherGuide;
}

// 过滤条件
export interface ActivityFilters {
  subject?: string;
  grade?: string;
  activity_type?: string;
}

export interface ScenarioFilters {
  subject?: string;
  grade?: string;
  scenario_type?: string;
}

// API方法
// 获取活动列表
export async function getActivities(filters: ActivityFilters = {}): Promise<Activity[]> {
  return request.get('/interactive/activities', { params: filters });
}

// 获取活动详情
export async function getActivity(id: string): Promise<Activity> {
  return request.get(`/interactive/activities/${id}`);
}

// 创建新活动
export interface CreateActivityRequest {
  activity_type: 'discussion' | 'question' | 'game';
  subject: string;
  grade: string;
  topic: string;
  duration: number;
}

export async function createActivity(data: CreateActivityRequest): Promise<Activity> {
  return request.post('/interactive/activities', data);
}

// 获取场景列表
export async function getScenarios(filters: ScenarioFilters = {}): Promise<Scenario[]> {
  return request.get('/interactive/scenarios', { params: filters });
}

// 获取场景详情
export async function getScenario(id: string): Promise<Scenario> {
  return request.get(`/interactive/scenarios/${id}`);
}

// 创建新场景
export interface CreateScenarioRequest {
  scenario_type: 'historical' | 'literary' | 'scientific';
  subject: string;
  grade: string;
  theme: string;
}

export async function createScenario(data: CreateScenarioRequest): Promise<Scenario> {
  return request.post('/interactive/scenarios', data);
}
