import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/teacher',
      component: () => import('@/layouts/TeacherLayout.vue'),
      children: [
        {
          path: 'exam',
          component: () => import('@/views/teacher/exam/ExamGenerator.vue')
        }
      ]
    }
  ]
})

export default router