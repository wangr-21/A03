import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api';

// 创建axios实例
export const request = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    // 可以在这里添加token等认证信息
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    // 统一处理错误
    console.error('API请求错误:', error);
    return Promise.reject(error);
  },
);

// 导出所有API模块
export * from './teaching';
export * from './interactive';
export * from './question';
export * from './case';
export * from './resource';
export * from './community';
export * from './user';
export * from './lab';
export * from './lighthouse';
export * from './thinking';
