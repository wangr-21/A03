import { request } from './index';
import type { UploadUserFile } from 'element-plus';
import labDemoAssets from '@/assets/lab';

export interface StyleOption {
  name: string;
  key: string;
  thumb: string;
}

export interface ColorAnalysisResponse {
  colors: {
    hex: string;
    percentage: number;
  }[];
  keywords: string[];
  dimensions: {
    [key: string]: number;
  };
}

export interface UploadResponse {
  success: boolean;
  url?: string;
  message?: string;
}

// 获取可用风格列表
export function getAvailableStyles(): StyleOption[] {
  return [
    { name: '印象派', key: 'impressionism', thumb: '/src/assets/icons/impressionism.png' },
    { name: '梵高', key: 'van_gogh', thumb: '/src/assets/icons/van_gogh.png' },
    { name: '水墨画', key: 'ink_wash', thumb: '/src/assets/icons/ink_wash.png' },
    { name: '赛博朋克', key: 'cyberpunk', thumb: '/src/assets/icons/cyberpunk.png' },
    { name: '浮世绘', key: 'ukiyo_e', thumb: '/src/assets/icons/ukiyo_e.png' },
  ];
}

// 上传图片
export async function uploadImage(file: File): Promise<UploadResponse> {
  // 真实环境下应该是:
  // const formData = new FormData();
  // formData.append('file', file);
  // return request.post('/upload', formData);

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 3000));

  return {
    success: true,
    url: URL.createObjectURL(file),
  };
}

// 应用风格转换
export async function applyStyleTransfer(imageFile: UploadUserFile, style: string): Promise<Blob> {
  // const formData = new FormData();
  // formData.append('style_prompt', style);
  // formData.append('file', imageFile.raw as File);
  // return request.post('/style-transfer/generate', formData, {
  //   responseType: 'blob',
  // });

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 2000));
  const images = labDemoAssets.image[style as keyof typeof labDemoAssets.image] as readonly string[];
  const response = await fetch(images[Math.floor(Math.random() * images.length)]);
  return response.blob();
}

// 分析色彩情感
export async function analyzeColorEmotion(
  imageFile: UploadUserFile,
): Promise<ColorAnalysisResponse> {
  // 真实环境下应该是:
  const formData = new FormData();
  formData.append('file', imageFile.raw as File);
  return request.post('/analysis/image', formData);
}

export async function demoGetImageEmotionAnalysis() {
  await new Promise((resolve) => setTimeout(resolve, 600));
  return labDemoAssets.emotion;
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
  await new Promise((resolve) => setTimeout(resolve, 6000));

  return {
    videoUrl: labDemoAssets.video[Math.floor(Math.random() * labDemoAssets.video.length)],
    script: `1. 画面拉近，聚焦主体。
2. 添加轻快背景音乐。
3. 元素[A]向右移动。
4. 画面淡出。`,
  };
}
