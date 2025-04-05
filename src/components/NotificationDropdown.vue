<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';

// 定义Props
defineProps({
  isActive: {
    type: Boolean,
    default: false,
  },
});

// 定义Emits
const emit = defineEmits(['close', 'readAll', 'viewAll']);

// 通知状态
const notifications = ref([
  {
    id: 1,
    type: 'message',
    title: '新消息',
    content: '张老师给您发送了一条消息',
    time: '10分钟前',
    avatar: '/src/assets/avatar1.svg',
    read: false,
  },
  {
    id: 2,
    type: 'comment',
    title: '评论回复',
    content: '李老师回复了您在"如何提高学生课堂参与度"的评论',
    time: '30分钟前',
    avatar: '/src/assets/avatar2.svg',
    read: false,
  },
  {
    id: 3,
    type: 'system',
    title: '系统通知',
    content: '您分享的资源"初中数学教案"已被审核通过',
    time: '2小时前',
    avatar: '/src/assets/system.svg',
    read: true,
  },
  {
    id: 4,
    type: 'comment',
    title: '评论回复',
    content: '王老师在师韵星盟点赞了您的评论',
    time: '昨天',
    avatar: '/src/assets/avatar3.svg',
    read: true,
  },
]);

// 未读消息数量
const unreadCount = ref(0);

// 计算未读消息数量
const calculateUnreadCount = () => {
  unreadCount.value = notifications.value.filter((notification) => !notification.read).length;
};

// 标记已读
const markAsRead = (id: number) => {
  const notification = notifications.value.find((item) => item.id === id);
  if (notification) {
    notification.read = true;
    calculateUnreadCount();
  }
};

// 标记全部已读
const markAllAsRead = () => {
  notifications.value.forEach((notification) => {
    notification.read = true;
  });
  calculateUnreadCount();
  emit('readAll');
};

// 查看所有通知
const viewAllNotifications = () => {
  emit('viewAll');
};

// 关闭下拉菜单
const closeDropdown = () => {
  emit('close');
};

// 点击外部关闭下拉菜单
const handleClickOutside = (event: MouseEvent) => {
  const dropdown = document.querySelector('.notification-dropdown');
  if (dropdown && !dropdown.contains(event.target as Node)) {
    closeDropdown();
  }
};

// 组件挂载后添加点击外部事件监听
onMounted(() => {
  calculateUnreadCount();
  document.addEventListener('click', handleClickOutside);
});

// 组件销毁前移除事件监听
onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<template>
  <div class="notification-dropdown" v-if="isActive">
    <div class="notification-header">
      <h3>
        通知中心 <span v-if="unreadCount > 0">({{ unreadCount }})</span>
      </h3>
      <button class="read-all-btn" @click="markAllAsRead" v-if="unreadCount > 0">全部已读</button>
    </div>

    <div class="notification-tabs">
      <button class="tab-btn active">全部</button>
      <button class="tab-btn">消息</button>
      <button class="tab-btn">评论</button>
      <button class="tab-btn">系统</button>
    </div>

    <div class="notification-list" v-if="notifications.length > 0">
      <div
        v-for="notification in notifications"
        :key="notification.id"
        class="notification-item"
        :class="{ unread: !notification.read }"
        @click="markAsRead(notification.id)"
      >
        <div class="notification-avatar">
          <img :src="notification.avatar" alt="头像" />
        </div>
        <div class="notification-content">
          <div class="notification-title">{{ notification.title }}</div>
          <div class="notification-text">{{ notification.content }}</div>
          <div class="notification-time">{{ notification.time }}</div>
        </div>
        <div class="notification-badge" v-if="!notification.read"></div>
      </div>
    </div>

    <div class="notification-empty" v-else>
      <el-icon><Bell /></el-icon>
      <p>暂无通知</p>
    </div>

    <div class="notification-footer">
      <button class="view-all-btn" @click="viewAllNotifications">查看全部通知</button>
    </div>
  </div>
</template>

<style scoped>
.notification-dropdown {
  position: absolute;
  top: 60px;
  right: 10px;
  width: 360px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  overflow: hidden;
  max-height: 500px;
  display: flex;
  flex-direction: column;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.notification-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.read-all-btn {
  background: none;
  border: none;
  color: #7353e5;
  cursor: pointer;
  font-size: 14px;
}

.notification-tabs {
  display: flex;
  border-bottom: 1px solid #f0f0f0;
}

.tab-btn {
  flex: 1;
  padding: 12px 8px;
  background: none;
  border: none;
  cursor: pointer;
  color: #606266;
  font-size: 14px;
  transition: all 0.3s;
}

.tab-btn.active {
  color: #7353e5;
  border-bottom: 2px solid #7353e5;
}

.notification-list {
  overflow-y: auto;
  max-height: 350px;
}

.notification-item {
  display: flex;
  padding: 16px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background-color 0.3s;
  position: relative;
}

.notification-item:hover {
  background-color: #f9f9f9;
}

.notification-item.unread {
  background-color: rgba(115, 83, 229, 0.05);
}

.notification-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 12px;
  flex-shrink: 0;
}

.notification-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.notification-content {
  flex: 1;
}

.notification-title {
  font-weight: 600;
  font-size: 14px;
  color: #333;
  margin-bottom: 4px;
}

.notification-text {
  font-size: 13px;
  color: #606266;
  margin-bottom: 4px;
  line-height: 1.4;
}

.notification-time {
  font-size: 12px;
  color: #999;
}

.notification-badge {
  position: absolute;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #f56c6c;
  top: 16px;
  right: 16px;
}

.notification-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  color: #909399;
}

.notification-empty .el-icon {
  font-size: 32px;
  margin-bottom: 16px;
  color: #dcdfe6;
}

.notification-footer {
  padding: 12px;
  text-align: center;
  border-top: 1px solid #f0f0f0;
}

.view-all-btn {
  width: 100%;
  background-color: #f5f7fa;
  border: none;
  padding: 8px;
  border-radius: 4px;
  cursor: pointer;
  color: #606266;
  transition: all 0.3s;
}

.view-all-btn:hover {
  background-color: #eceff5;
  color: #7353e5;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .notification-dropdown {
    width: 100%;
    right: 0;
    top: 64px;
    max-height: calc(100vh - 64px);
    border-radius: 0;
  }
}
</style>
