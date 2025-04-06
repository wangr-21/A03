import { ref, computed } from 'vue';
import { getNotifications, markAllNotificationsAsRead } from '@/api';
import type { Notification } from '@/api';
import { ElMessage } from 'element-plus';

export function useNotifications() {
  const showNotificationDropdown = ref(false);
  const notifications = ref<Notification[]>([]);
  const unreadCount = ref(0);
  const hasNotifications = computed(() => unreadCount.value > 0);

  const toggleNotificationDropdown = async () => {
    if (!showNotificationDropdown.value) {
      await fetchNotifications();
    }
    showNotificationDropdown.value = !showNotificationDropdown.value;
  };

  const closeNotificationDropdown = () => {
    showNotificationDropdown.value = false;
  };

  const fetchNotifications = async () => {
    try {
      const response = await getNotifications();
      if (response.success) {
        notifications.value = response.data.notifications;
        unreadCount.value = response.data.unreadCount;
      } else {
        throw new Error('Failed to fetch notifications');
      }
    } catch (error) {
      console.error('Error fetching notifications:', error);
    }
  };

  const markAllAsRead = async () => {
    try {
      const response = await markAllNotificationsAsRead();
      if (response.success) {
        unreadCount.value = 0;
        // 更新通知状态
        notifications.value = notifications.value.map((n) => ({ ...n, read: true }));
        ElMessage.success('已将所有通知标记为已读');
      }
    } catch (error) {
      console.error('Error marking notifications as read:', error);
      ElMessage.error('操作失败，请稍后重试');
    }
  };

  const viewAllNotifications = () => {
    // 可以导航到通知页面
    console.log('View all notifications');
    closeNotificationDropdown();
  };

  // 初始加载通知
  const initialize = () => {
    fetchNotifications();
  };

  return {
    showNotificationDropdown,
    notifications,
    unreadCount,
    hasNotifications,
    toggleNotificationDropdown,
    closeNotificationDropdown,
    markAllAsRead,
    viewAllNotifications,
    initialize,
  };
}
