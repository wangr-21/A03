import { request } from './index';

export interface InteractionItem {
  type: string;
  title: string;
  content: string[];
}

export interface InteractionResponse {
  success: boolean;
  data: InteractionItem[];
}

// 获取推荐互动
export async function getRecommendedInteractions(topic: string): Promise<InteractionItem[]> {
  return request.get('/interactive/recommendations', { params: { topic } });
}
