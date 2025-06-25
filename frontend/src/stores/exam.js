import { defineStore } from 'pinia'
import axios from 'axios'

export const useExamStore = defineStore('exam', {
  state: () => ({
    examList: [],
    currentExam: null
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