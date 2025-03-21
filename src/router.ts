import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import TeacherWorkbench from './components/TeacherWorkbench.vue';
import ResourceCenter from './components/ResourceCenter.vue';
import DataAnalysis from './components/DataAnalysis.vue';
import Home from './components/Home.vue';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/workbench',
    name: 'TeacherWorkbench',
    component: TeacherWorkbench,
  },
  {
    path: '/resources',
    name: 'ResourceCenter',
    component: ResourceCenter,
  },
  {
    path: '/analysis',
    name: 'DataAnalysis',
    component: DataAnalysis,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
