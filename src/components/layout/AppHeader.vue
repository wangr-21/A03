<script setup lang="ts">
import { useUserStore } from '@/stores/userStore';
import { useNotifications } from '@/hooks/useNotifications';
import { useSettings } from '@/hooks/useSettings';
import NotificationDropdown from '@/components/NotificationDropdown.vue';
import SettingsDropdown from '@/components/SettingsDropdown.vue';
import BreadCrumb from './BreadCrumb.vue';
import { onMounted } from 'vue';
import { avatar0 } from '@/assets/avatars';

defineProps({
  isMobile: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits<{
  toggleSidebar: [];
}>();

const {
  showNotificationDropdown,
  hasNotifications,
  toggleNotificationDropdown,
  closeNotificationDropdown,
  markAllAsRead,
  viewAllNotifications,
  initialize,
} = useNotifications();

const { showSettingsDropdown, toggleSettingsDropdown, closeSettingsDropdown } =
  useSettings(showNotificationDropdown);

onMounted(() => initialize());

// 获取用户状态
const userStore = useUserStore();

// 检查用户登录状态
onMounted(() => userStore.initUserState());
</script>

<template>
  <header class="header">
    <!-- 移动端菜单按钮 -->
    <div class="mobile-menu-toggle" v-if="isMobile" @click="emit('toggleSidebar')">
      <el-icon><Menu /></el-icon>
    </div>

    <!-- 面包屑 -->
    <BreadCrumb :is-mobile="isMobile" />

    <div class="right-tools">
      <div class="notification-icon-wrapper">
        <el-badge is-dot :hidden="!hasNotifications">
          <el-icon class="tool-icon" @click="toggleNotificationDropdown"><Bell /></el-icon>
        </el-badge>
        <NotificationDropdown
          :is-active="showNotificationDropdown"
          @close="closeNotificationDropdown"
          @read-all="markAllAsRead"
          @view-all="viewAllNotifications"
        />
      </div>
      <div class="settings-icon-wrapper">
        <el-icon class="tool-icon" @click="toggleSettingsDropdown"><Setting /></el-icon>
        <SettingsDropdown :is-active="showSettingsDropdown" @close="closeSettingsDropdown" />
      </div>
      <div class="user-avatar" @click="toggleSettingsDropdown">
        <img
          :src="userStore.userInfo?.avatar || avatar0"
          :alt="userStore.userInfo?.name || '用户头像'"
        />
      </div>
    </div>
  </header>
</template>

<style scoped>
.header {
  height: 64px;
  background-color: white;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.5rem;
  position: sticky;
  top: 0;
  z-index: 10;
}

.mobile-menu-toggle {
  display: none;
}

:deep(.app-container.mobile) .mobile-menu-toggle {
  display: block;
  font-size: 1.5rem;
  cursor: pointer;
}

.right-tools {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.tool-icon {
  font-size: 1.375rem;
  color: #606266;
  cursor: pointer;
  display: flex;
  align-items: center;
  height: 2.25rem;
}

.user-avatar {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 50%;
  overflow: hidden;
  box-shadow: 0 0 0 2px rgba(115, 83, 229, 0.2);
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.user-avatar:hover {
  transform: scale(1.05);
}
</style>
