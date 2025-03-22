import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('./components/Home.vue'),
    },
    {
      path: '/workbench',
      component: () => import('./components/TeacherWorkbench.vue'),
    },
    {
      path: '/resources',
      component: () => import('./components/ResourceCenter.vue'),
    },
    {
      path: '/analysis',
      component: () => import('./components/DataAnalysis.vue'),
    },
  ],
});

export default router;
