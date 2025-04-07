<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { ElMessage } from 'element-plus';
import type { FormInstance, FormRules } from 'element-plus';
import { login } from '@/api';
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

// 获取重定向路径
onMounted(() => {
  if (route.query.redirect && typeof route.query.redirect === 'string') {
    redirectPath.value = route.query.redirect;
  }
});

// 登录提交
const handleLogin = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;

  await formEl.validate(async (valid) => {
    if (!valid) return;

    loading.value = true;

    try {
      const response = await login(loginForm);
      if (response.success) {
        // 存储token
        localStorage.setItem('token', response.data.token);

        // 存储用户信息
        localStorage.setItem('userInfo', JSON.stringify(response.data.userInfo));

        // 登录成功提示
        ElMessage.success('登录成功，欢迎回来！');

        // 跳转到重定向页面或首页
        router.replace(redirectPath.value);
      }
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
    } catch (error: any) {
      ElMessage.error(error.message || '登录失败，请重试');
    } finally {
      loading.value = false;
    }
  });
};

// 快速演示登录
const quickDemoLogin = () => {
  loginForm.username = 'teacher';
  loginForm.password = '123456';
  loginFormRef.value?.validate(() => {
    handleLogin(loginFormRef.value);
  });
};
</script>

<template>
  <div class="login-container">
    <div class="login-content">
      <div class="login-header">
        <h1 class="app-title">师韵星盟</h1>
        <p class="app-slogan">汇聚教育智慧 · 点亮教学星火</p>
      </div>

      <el-card class="login-card">
        <template #header>
          <div class="card-header">
            <h2>登录账号</h2>
          </div>
        </template>

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

          <el-form-item>
            <div class="form-footer">
              <el-checkbox v-model="loginForm.rememberMe" :disabled="loading">记住我</el-checkbox>
              <el-button type="text" :disabled="loading">忘记密码?</el-button>
            </div>
          </el-form-item>

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
              class="demo-button"
              :disabled="loading"
              @click="quickDemoLogin"
            >
              演示账号快速登录
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <div class="login-footer">
        <p>首次使用请联系管理员获取账号 | 技术支持: 智慧教育平台</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
}

.login-content {
  width: 100%;
  max-width: 460px;
  text-align: center;
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
}

.app-slogan {
  margin-top: 10px;
  color: #666;
  font-size: 16px;
}

.login-card {
  border-radius: 10px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  background-color: #fff;
  margin-bottom: 20px;
}

.card-header {
  text-align: center;
  padding: 15px 0;
}

.card-header h2 {
  font-size: 22px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.login-form {
  padding: 20px 30px;
}

.form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.login-button {
  width: 100%;
  border-radius: 4px;
  font-weight: 500;
  letter-spacing: 1px;
}

.demo-button {
  width: 100%;
  border-radius: 4px;
}

.login-footer {
  margin-top: 20px;
  color: #666;
  font-size: 14px;
}

/* 响应式调整 */
@media (max-width: 480px) {
  .login-content {
    max-width: 100%;
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
}
</style>
