<script setup lang="ts">
import { ref, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/userStore';
import { ElMessage, ElMessageBox } from 'element-plus';

// 定义属性和事件
defineProps<{
  isActive: boolean;
}>();

const emit = defineEmits(['close']);

const router = useRouter();
const userStore = useUserStore();

// 获取用户信息
const userInfo = ref(userStore.userInfo);

// 切换深色/浅色模式
const isDarkMode = ref(false);
const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value;
  // 实际应用中，这里可以切换文档的class或应用主题
  document.documentElement.classList.toggle('dark-mode', isDarkMode.value);
  ElMessage.success(`已切换到${isDarkMode.value ? '深色' : '浅色'}模式`);
};

// 打开个人资料页
const openUserProfile = () => {
  emit('close');
  // TODO: 这里可以导航到个人资料页
  ElMessage.info('即将开发个人资料页面');
};

// 打开系统设置页
const openSystemSettings = () => {
  emit('close');
  // TODO: 这里可以导航到系统设置页
  ElMessage.info('即将开发系统设置页面');
};

// 退出登录
const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    });

    await userStore.userLogout();
    emit('close');
    router.push('/login');
  } catch {
    // 用户取消，不做任何操作
  }
};

// 点击外部关闭下拉菜单
const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as HTMLElement;
  if (!target.closest('.settings-dropdown') && !target.closest('.tool-icon')) {
    emit('close');
  }
};

// 添加全局点击事件监听器
document.addEventListener('click', handleClickOutside);
// 组件卸载时移除事件监听器
onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<template>
  <div class="settings-dropdown" v-if="isActive">
    <div class="dropdown-header">
      <div class="user-info">
        <el-avatar :size="50" :src="userInfo?.avatar || '/src/assets/avatar.svg'"></el-avatar>
        <div class="user-details">
          <h3>{{ userInfo?.name || '用户名' }}</h3>
          <p>{{ userInfo?.title || '职位' }}</p>
        </div>
      </div>
    </div>

    <div class="dropdown-content">
      <el-divider>设置选项</el-divider>
      <ul class="settings-list">
        <li @click="openUserProfile">
          <el-icon><User /></el-icon>
          <span>个人资料</span>
        </li>
        <li @click="openSystemSettings">
          <el-icon><Setting /></el-icon>
          <span>系统设置</span>
        </li>
        <li @click="toggleDarkMode">
          <el-icon v-if="isDarkMode"><Sunrise /></el-icon>
          <el-icon v-else><Moon /></el-icon>
          <span>{{ isDarkMode ? '切换浅色模式' : '切换深色模式' }}</span>
        </li>
      </ul>
    </div>

    <div class="dropdown-footer">
      <el-button type="danger" text @click="handleLogout">
        <el-icon><SwitchButton /></el-icon>
        退出登录
      </el-button>
    </div>
  </div>
</template>

<style scoped>
.settings-dropdown {
  position: absolute;
  top: 60px;
  right: 10px;
  width: 320px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  overflow: hidden;
  animation: fadeInDown 0.3s ease-out;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-header {
  padding: 20px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #eee;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-details h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.user-details p {
  margin: 4px 0 0;
  font-size: 14px;
  color: #666;
}

.dropdown-content {
  padding: 10px 0;
}

.settings-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.settings-list li {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.settings-list li:hover {
  background-color: #f5f7fa;
}

.settings-list li .el-icon {
  margin-right: 12px;
  font-size: 18px;
  color: #7353e5;
}

.settings-list li span {
  font-size: 14px;
  color: #333;
}

.dropdown-footer {
  padding: 10px 20px;
  border-top: 1px solid #eee;
  text-align: center;
}
</style>
