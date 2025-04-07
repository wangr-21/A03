import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '@/stores/userStore';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL || '/'),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
      meta: { title: '启智学堂', requiresAuth: true },
    },
    {
      path: '/workshop',
      name: 'workshop',
      component: () => import('../views/WorkshopView.vue'),
      meta: { title: '智课工坊', requiresAuth: true },
    },
    {
      path: '/lab',
      name: 'lab',
      component: () => import('../views/LabView.vue'),
      meta: { title: '幻画实验室', requiresAuth: true },
    },
    {
      path: '/lighthouse',
      name: 'lighthouse',
      component: () => import('../views/LighthouseView.vue'),
      meta: { title: '学海灯塔', requiresAuth: true },
    },
    {
      path: '/community',
      name: 'community',
      component: () => import('../views/CommunityView.vue'),
      meta: { title: '师韵星盟', requiresAuth: true },
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { title: '登录 - 师韵星盟', hideLayout: true },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      redirect: '/',
    },
  ],
});

// 设置页面标题和权限检查
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = (to.meta.title as string | undefined) || '启智学堂';

  // 检查该路由是否需要登录
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    // 获取用户状态
    const userStore = useUserStore();
    userStore.initUserState(); // 初始化用户状态

    // 如果用户未登录，重定向到登录页面
    if (!userStore.isLoggedIn) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }, // 将要访问的页面路径传递给登录页面
      });
    } else {
      next(); // 已登录，继续导航
    }
  } else {
    // 不需要登录的路由，直接进入
    next();
  }
});

export default router;
