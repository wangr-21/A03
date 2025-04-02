import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
      meta: { title: '启智学堂' }
    },
    {
      path: '/workshop',
      name: 'workshop',
      component: () => import('../views/WorkshopView.vue'),
      meta: { title: '智课工坊' }
    },
    {
      path: '/lab',
      name: 'lab',
      component: () => import('../views/LabView.vue'),
      meta: { title: '幻画实验室' }
    },
    {
      path: '/lighthouse',
      name: 'lighthouse',
      component: () => import('../views/LighthouseView.vue'),
      meta: { title: '学海灯塔' }
    },
    {
      path: '/community',
      name: 'community',
      component: () => import('../views/CommunityView.vue'),
      meta: { title: '师韵星盟' }
    }
  ]
})

// 设置页面标题
router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title || 'XXXX教育平台'}`
  next()
})

export default router
