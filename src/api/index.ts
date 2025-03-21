import axios from "axios";

const BASE_URL = "http://localhost:8000/api";

type ApiResponse<T> =
  | {
      success: true;
      data: T;
    }
  | {
      success: false;
      error: string;
    };

const api = {
  generateTeachingPlan: async (params: {
    subject: string;
    grade: string;
    topic: string;
  }): Promise<ApiResponse<string>> => {
    try {
      const response = await axios.post<{
        success: true;
        data: string;
      }>(`${BASE_URL}/teaching/generate-plan`, params);
      return response.data;
    } catch (error: any) {
      console.error("API调用错误:", error.response?.data || error.message);
      return {
        success: false,
        error: error.response?.data?.detail || "服务器错误",
      };
    }
  },
  generateTeachingImage: async (
    prompt: string
  ): Promise<ApiResponse<object>> => {
    try {
      const response = await axios.post<{
        success: true;
        data: object;
      }>(`${BASE_URL}/teaching/generate-image`, {
        text: prompt,
      });
      return response.data;
    } catch (error: any) {
      console.error("API调用错误:", error.message);
      return {
        success: false,
        error: "服务器错误",
      };
    }
  },
  queryKnowledgeGraph: async (query: string) => {
    try {
      const response = await axios.post(`${BASE_URL}/knowledge/query`, {
        query,
      });
      return response.data;
    } catch (error: any) {
      console.error("API调用错误:", error.message);
      return {
        success: false,
        error: "服务器错误",
      };
    }
  },
};

export default api;
