import { defineStore } from 'pinia'
import axios from 'axios'

export const useExamStore = defineStore('exam', {
  state: () => ({
    examList: [],
    currentExam: null,
    courseOptions: [
      { id: 1, name: '计算机网络' },
      { id: 2, name: '操作系统' },
      { id: 3, name: '数据结构' }
    ],
    knowledgePointMap: {
      1: ['TCP/IP协议', '网络安全', '路由协议'],
      2: ['进程管理', '内存管理', '文件系统'],
      3: ['链表', '树', '图', '排序算法']
    }
  }),
  
  actions: {
    async generateExam(config) {
      const response = await axios.post('/api/v1/exams/generate', config)
      return response.data
    },
    
    async saveExam(exam) {
      const response = await axios.post('/api/v1/exams', exam)
      return response.data
    }
  }
})