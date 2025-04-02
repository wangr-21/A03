import { request } from './index';
import type { UploadUserFile } from 'element-plus';

export interface StyleOption {
  name: string;
  key: string;
  thumb: string;
}

export interface ColorAnalysisResultType {
  radarData: number[];
  keywords: string[];
  dominantColors: string[];
}

export interface UploadResponse {
  success: boolean;
  url?: string;
  message?: string;
}

// 获取可用风格列表
export function getAvailableStyles(): StyleOption[] {
  return [
    { name: '印象派', key: 'impressionism', thumb: '/src/assets/style_thumb1.jpg' },
    { name: '梵高', key: 'van_gogh', thumb: '/src/assets/style_thumb2.jpg' },
    { name: '水墨画', key: 'ink_wash', thumb: '/src/assets/style_thumb3.jpg' },
    { name: '赛博朋克', key: 'cyberpunk', thumb: '/src/assets/style_thumb4.jpg' },
    { name: '浮世绘', key: 'ukiyo_e', thumb: '/src/assets/style_thumb5.jpg' },
  ];
}

// 上传图片
export async function uploadImage(file: File): Promise<UploadResponse> {
  // 真实环境下应该是:
  // const formData = new FormData();
  // formData.append('file', file);
  // return request.post('/upload', formData);

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 300));

  return {
    success: true,
    url: URL.createObjectURL(file),
  };
}

// 应用风格转换
export async function applyStyleTransfer(
  imageFile: UploadUserFile,
  style: string,
): Promise<{ resultUrl: string }> {
  // 真实环境下应该是:
  // const formData = new FormData();
  // formData.append('image', imageFile.raw as File);
  // formData.append('style', style);
  // return request.post('/lab/style-transfer', formData);

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 3000));

  return {
    resultUrl: '/src/assets/styled_result.jpg', // Placeholder result
  };
}

// 分析色彩情感
export async function analyzeColorEmotion(
  imageFile: UploadUserFile,
): Promise<ColorAnalysisResultType> {
  // 真实环境下应该是:
  // const formData = new FormData();
  // formData.append('image', imageFile.raw as File);
  // return request.post('/lab/color-analysis', formData);

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 2000));

  return {
    radarData: [80, 60, 75, 50, 90], // Example: Warmth, Brightness, Contrast, Saturation, Harmony
    keywords: ['活泼', '明亮', '温暖', '积极', '对比强烈'],
    dominantColors: ['#FF7A5A', '#FFB64D', '#FFFFFF', '#7353E5'],
  };
}

// 生成视频
export async function generateVideo(
  imageFile: UploadUserFile,
  music?: string,
): Promise<{ videoUrl: string; script: string }> {
  // 真实环境下应该是:
  // const formData = new FormData();
  // formData.append('image', imageFile.raw as File);
  // if (music) formData.append('music', music);
  // return request.post('/lab/generate-video', formData);

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 5000));

  return {
    videoUrl: '/src/assets/generated_video.mp4',
    script: `1. 画面拉近，聚焦主体。
2. 添加轻快背景音乐。
3. 元素[A]向右移动。
4. 画面淡出。`,
  };
}
