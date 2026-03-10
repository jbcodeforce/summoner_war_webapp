import { createRouter, createWebHistory } from 'vue-router'
import GamesView from '../views/GamesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'games',
      component: GamesView,
    },
    {
      path: '/matrix',
      name: 'matrix',
      component: () => import('../views/MatrixView.vue'),
    },
    {
      path: '/factions',
      name: 'factions',
      component: () => import('../views/FactionsView.vue'),
    },
  ],
})

export default router
