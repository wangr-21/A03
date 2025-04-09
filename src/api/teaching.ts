import { request } from './index';

// 生成教案响应
export interface GeneratePlanResponse {
  plan_id: string;
  plan: string;
}

// 生成教案
export async function generateLessonPlan(
  grade: string,
  images: File[],
): Promise<GeneratePlanResponse> {
  const formData = new FormData();
  formData.append('grade', grade);

  // 添加所有图片
  images.forEach((file) => {
    formData.append('images', file);
  });

  return request.post('/teaching/generate_plan', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
}

// 导出Word文档
export async function exportPlanAsDocx(planId: string): Promise<Blob> {
  return request.get(`/teaching/plan_document/${planId}`, {
    responseType: 'blob',
  });
}
