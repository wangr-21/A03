import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = {
    // 生成教学计划
    generateTeachingPlan: async (subject, grade, topic) => {
        try {
            const response = await axios.post(`${API_BASE_URL}/api/teaching-plan`, {
                subject,
                grade,
                topic
            });
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // 生成教学图片
    generateTeachingImage: async (prompt) => {
        try {
            const response = await axios.post(`${API_BASE_URL}/api/teaching-image`, {
                prompt
            });
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // 查询知识图谱
    queryKnowledgeGraph: async (query) => {
        try {
            const response = await axios.post(`${API_BASE_URL}/api/knowledge-graph`, {
                query
            });
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    // 预测学习状态
    predictLearningStatus: async (studentData) => {
        try {
            const response = await axios.post(`${API_BASE_URL}/api/learning-status`, studentData);
            return response.data;
        } catch (error) {
            throw error;
        }
    }
};

export default api;