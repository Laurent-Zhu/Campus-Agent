import { createRouter, createWebHistory } from 'vue-router'
import TeacherLayout from '@/layouts/TeacherLayout.vue'

const routes = [
  // 默认主页
  {
    path: '/',
    name: 'Home',
    component: () => import('@/components/HelloWorld.vue')
  },
  // 教师工作台布局及子页面
  {
    path: '/teacher',
    component: TeacherLayout,
    children: [
      {
        path: 'exam',
        name: 'TeacherExam',
        component: () => import('@/pages/teacher/ExamList.vue') // 考核管理页面
      },
      {
        path: 'exam-generate',
        name: 'ExamGenerator',
        component: () => import('@/pages/teacher/ExamGeneratorNew.vue') // 生成考核页面
      }
      // 可继续添加教师端其它子页面
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/pages/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/pages/Register.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router