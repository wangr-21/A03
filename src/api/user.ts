import { request } from './index';

export interface Notification {
  id: number;
  type: string;
  title: string;
  content: string;
  time: string;
  avatar: string;
  read: boolean;
}

export interface NotificationsResponse {
  success: boolean;
  data: {
    notifications: Notification[];
    unreadCount: number;
  };
}

// 获取通知列表
export async function getNotifications(): Promise<NotificationsResponse> {
  // 真实环境下应该是:
  // return request.get('/user/notifications');

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 500));

  const notifications: Notification[] = [
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
      content: '您上传的教案已通过审核',
      time: '2小时前',
      avatar: '/src/assets/system.svg',
      read: true,
    },
  ];

  const unreadCount = notifications.filter((n) => !n.read).length;

  return {
    success: true,
    data: {
      notifications,
      unreadCount,
    },
  };
}

// 标记通知为已读
export async function markNotificationAsRead(
  notificationId: number,
): Promise<{ success: boolean }> {
  // 真实环境下应该是:
  // return request.put(`/user/notifications/${notificationId}/read`);

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 200));

  return {
    success: true,
  };
}

// 标记所有通知为已读
export async function markAllNotificationsAsRead(): Promise<{ success: boolean }> {
  // 真实环境下应该是:
  // return request.put('/user/notifications/read-all');

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 300));

  return {
    success: true,
  };
}
