<script setup lang="ts">
import { ref, reactive, onMounted, onBeforeUnmount } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { ElMessage } from 'element-plus';
import type { FormInstance, FormRules } from 'element-plus';
import { login,getCurrentUser  } from '@/api';
import type { LoginForm } from '@/api';

const router = useRouter();
const route = useRoute();

// 登录表单
const loginForm = reactive<LoginForm>({
  username: '',
  password: '',
  rememberMe: false,
});

// 表单验证规则
const loginRules = reactive<FormRules>({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应在3-20个字符之间', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应在6-20个字符之间', trigger: 'blur' },
  ],
});

// 登录状态
const loading = ref(false);
const loginFormRef = ref<FormInstance>();
const redirectPath = ref('/');

// 获取重定向路径并处理页面样式
onMounted(() => {
  if (route.query.redirect && typeof route.query.redirect === 'string') {
    redirectPath.value = route.query.redirect;
  }

  // 固定页面，防止滚动和移动
  document.documentElement.style.overflow = 'hidden';
  document.body.style.overflow = 'hidden';
  document.body.style.position = 'fixed';
  document.body.style.width = '100%';
  document.body.style.height = '100%';
});

// 组件卸载时恢复页面样式
onBeforeUnmount(() => {
  document.documentElement.style.overflow = '';
  document.body.style.overflow = '';
  document.body.style.position = '';
  document.body.style.width = '';
  document.body.style.height = '';
});

// 登录提交
const handleLogin = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;

  await formEl.validate(async (valid) => {
    if (!valid) return;

    loading.value = true;

    try {
      const response = await login(loginForm);
        // 存储token
        localStorage.setItem('token', response.access_token);

      const userInfo = await getCurrentUser();
        // 存储用户信息
        localStorage.setItem('userInfo', JSON.stringify(userInfo));

        // 登录成功提示
        ElMessage.success('登录成功，欢迎回来！');

        // 跳转到重定向页面或首页
        router.replace(redirectPath.value);
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
    } catch (error: any) {
      ElMessage.error(error.message || '登录失败，请重试');
    } finally {
      loading.value = false;
    }
  });
};

// 处理忘记密码
const handleForgotPassword = () => {
  ElMessage({
    message: '请联系管理员重置密码',
    type: 'info',
    duration: 5000,
    showClose: true,
    grouping: true,
  });
  // 可以在这里添加更多逻辑，如显示重置密码对话框或导航到密码重置页面
  // router.push('/reset-password');
};

// 添加注册处理函数
const handleRegister = () => {
  router.push('/register');
};
</script>

<template>
  <div class="login-page">
    <div class="login-background">
      <!-- 背景装饰元素 -->
      <div class="bg-circle circle-1"></div>
      <div class="bg-circle circle-2"></div>
      <div class="bg-circle circle-3"></div>
    </div>

    <div class="login-container">
      <div class="login-content">
        <div class="login-header">
          <h1 class="app-title">艺智绘</h1>
          <p class="app-slogan">汇聚教育智慧 · 点亮教学星火</p>
        </div>

        <el-card class="login-card">
          <div class="custom-card-header">
            <div class="header-decoration left"></div>
            <h2 class="header-title">登录账号</h2>
            <div class="header-decoration right"></div>
          </div>

          <el-form
            ref="loginFormRef"
            :model="loginForm"
            :rules="loginRules"
            label-width="0"
            class="login-form"
          >
            <el-form-item prop="username">
              <el-input
                v-model="loginForm.username"
                placeholder="用户名"
                prefix-icon="User"
                size="large"
                :disabled="loading"
              />
            </el-form-item>

            <el-form-item prop="password">
              <el-input
                v-model="loginForm.password"
                type="password"
                placeholder="密码"
                prefix-icon="Lock"
                size="large"
                show-password
                :disabled="loading"
                @keyup.enter="handleLogin(loginFormRef)"
              />
            </el-form-item>

            <div class="auth-options">
              <el-checkbox v-model="loginForm.rememberMe" :disabled="loading" class="remember-me">
                记住我
              </el-checkbox>
              <el-button
                type="text"
                :disabled="loading"
                class="forgot-password"
                @click="handleForgotPassword"
              >
                忘记密码?
              </el-button>
            </div>

            <el-form-item>
              <el-button
                type="primary"
                :loading="loading"
                class="login-button"
                size="large"
                @click="handleLogin(loginFormRef)"
              >
                登录
              </el-button>
            </el-form-item>

            <el-form-item>
              <el-button
                type="info"
                plain
                size="large"
                class="register-button"
                :disabled="loading"
                @click="handleRegister"
              >
                注册账号
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <div class="login-footer">
          <p>首次使用请联系管理员获取账号 | 技术支持: 智慧教育平台</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 2000; /* 确保在所有元素之上 */
  overflow: hidden;
}

.login-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  overflow: hidden;
}

/* 背景装饰 */
.bg-circle {
  position: absolute;
  border-radius: 50%;
  opacity: 0.1;
  background: linear-gradient(135deg, #7353e5, #54d6ff);
}

.circle-1 {
  width: 300px;
  height: 300px;
  top: -100px;
  left: -100px;
  animation: float 20s infinite ease-in-out;
}

.circle-2 {
  width: 500px;
  height: 500px;
  bottom: -200px;
  right: -200px;
  animation: float 25s infinite ease-in-out reverse;
}

.circle-3 {
  width: 200px;
  height: 200px;
  top: 50%;
  left: 25%;
  animation: float 18s infinite ease-in-out;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-20px) scale(1.05);
  }
}

.login-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  box-sizing: border-box;
  padding: 20px;
}

.login-content {
  width: 100%;
  max-width: 460px;
  text-align: center;
  position: relative;
  z-index: 10;
  transition: all 0.3s ease;
}

.login-header {
  margin-bottom: 30px;
}

.app-title {
  font-size: 36px;
  font-weight: bold;
  color: #333;
  margin: 0;
  text-shadow: 1px 1px 1px rgba(0, 0, 0, 0.1);
  letter-spacing: 2px;
  animation: fadeInDown 0.8s ease;
}

.app-slogan {
  margin-top: 10px;
  color: #666;
  font-size: 16px;
  animation: fadeInUp 0.8s ease;
}

.login-card {
  border-radius: 10px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  background-color: #fff;
  margin-bottom: 20px;
  transform: translateY(0);
  opacity: 1;
  animation: fadeIn 0.8s ease;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.custom-card-header {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px 0;
  position: relative;
  background: #fff;
  border-bottom: 1px solid rgba(115, 83, 229, 0.1);
}

.header-decoration {
  height: 2px;
  width: 40px;
  background: linear-gradient(to right, transparent, #7353e5);
  margin: 0 15px;
  position: relative;
}

.header-decoration::before {
  content: '';
  position: absolute;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #7353e5;
  top: -2px;
}

.header-decoration.left {
  background: linear-gradient(to right, #7353e5, transparent);
}

.header-decoration.left::before {
  left: 0;
}

.header-decoration.right::before {
  right: 0;
}

.header-title {
  font-size: 24px;
  font-weight: 600;
  color: #7353e5;
  margin: 0;
  padding: 0 10px;
  position: relative;
  background: linear-gradient(135deg, #7353e5, #54d6ff);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: 2px;
}

.header-title::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 30px;
  height: 3px;
  background: linear-gradient(to right, #7353e5, #54d6ff);
  border-radius: 3px;
}

.login-form {
  padding: 25px 30px;
}

.auth-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 5px;
}

.remember-me {
  transition: transform 0.2s;
}

.remember-me:hover {
  transform: scale(1.02);
}

.forgot-password {
  color: #7353e5;
  padding: 8px 15px;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.forgot-password:hover {
  background-color: rgba(115, 83, 229, 0.1);
  color: #6040c8;
}

.login-button {
  width: 100%;
  border-radius: 4px;
  font-weight: 500;
  letter-spacing: 1px;
  background: linear-gradient(to right, #7353e5, #6b42e8);
  border: none;
  height: 44px;
  transition: all 0.3s ease;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 7px 14px rgba(115, 83, 229, 0.2);
}

.register-button {
  width: 100%;
  border-radius: 4px;
}

.login-footer {
  margin-top: 20px;
  color: #666;
  font-size: 14px;
  animation: fadeInUp 1s ease;
}

/* 动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式调整 */
@media (max-width: 480px) {
  .login-content {
    max-width: 100%;
    padding: 0 10px;
  }

  .app-title {
    font-size: 28px;
  }

  .app-slogan {
    font-size: 14px;
  }

  .login-form {
    padding: 15px;
  }

  .auth-options {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .forgot-password {
    padding-left: 0;
  }
}

/* 针对不同设备高度的调整 */
@media (max-height: 600px) {
  .login-content {
    transform: scale(0.9);
  }
}

@media (min-width: 992px) {
  .login-content {
    transform: translateY(-20px); /* 桌面版略微上移，视觉效果更好 */
  }
}
</style>
