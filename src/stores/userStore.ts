import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { getCurrentUser, logout } from '@/api';
import type { UserInfo } from '@/api';
import { ElMessage } from 'element-plus';

export const useUserStore = defineStore('user', () => {
  // 用户信息状态
  const userInfo = ref<UserInfo | null>(null);
  const token = ref<string | null>(null);
  const loading = ref<boolean>(false);

  // 计算属性：判断用户是否已登录
  const isLoggedIn = computed(() => !!token.value);

  // 初始化用户状态（从本地存储加载）
  const initUserState = () => {
    // 从localStorage获取token
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      token.value = storedToken;

      // 尝试从localStorage获取用户信息
      const storedUserInfo = localStorage.getItem('userInfo');
      if (storedUserInfo) {
        try {
          userInfo.value = JSON.parse(storedUserInfo);
        } catch (error) {
          console.error('Failed to parse user info:', error);
          userInfo.value = null;
        }
      }
    }
  };

  // 获取当前用户信息
  const fetchCurrentUser = async () => {
    if (!token.value) return;

    loading.value = true;
    try {
      const response = await getCurrentUser();
      userInfo.value = response;
      // 更新localStorage中的用户信息
      localStorage.setItem('userInfo', JSON.stringify(response));
    } catch (error) {
      console.error('Failed to fetch current user:', error);
      // 如果获取用户信息失败，清除token和用户信息
      clearUserState();
    } finally {
      loading.value = false;
    }
  };

  // 用户退出登录
  const userLogout = async () => {
    loading.value = true;
    try {
      await logout();
      clearUserState();
      ElMessage.success('已成功退出登录');
    } catch (error) {
      console.error('Logout failed:', error);
      // 即使API调用失败，也清除本地状态
      clearUserState();
    } finally {
      loading.value = false;
    }
  };

  // 清除用户状态
  const clearUserState = () => {
    token.value = null;
    userInfo.value = null;
    localStorage.removeItem('token');
    localStorage.removeItem('userInfo');
  };

  // 返回store的状态和方法
  return {
    userInfo,
    token,
    loading,
    isLoggedIn,
    initUserState,
    fetchCurrentUser,
    userLogout,
    clearUserState,
  };
});
