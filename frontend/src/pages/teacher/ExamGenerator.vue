<template>
  <div class="exam-generator">
    <el-card class="form-card">
      <el-form :model="examConfig" label-width="120px">
        <!-- 课程选择 -->
        <el-form-item label="选择课程">
          <el-select
            v-model="examConfig.courseId"
            placeholder="请选择课程"
            @change="onCourseChange"
            style="width: 100%"
          >
            <el-option
              v-for="course in courseOptions"
              :key="course.id"
              :label="course.name"
              :value="course.id"
            />
          </el-select>
        </el-form-item>
        <!-- 知识点选择 -->
        <el-form-item label="知识点">
          <el-select
            v-model="examConfig.knowledgePoints"
            multiple
            placeholder="请选择知识点"
            :disabled="!examConfig.courseId"
            style="width: 100%"
          >
            <el-option
              v-for="point in currentKnowledgePoints"
              :key="point"
              :label="point"
              :value="point"
            />
          </el-select>
        </el-form-item>
        <!-- 题型配置 -->
        <el-form-item label="题型配置">
          <div v-for="type in questionTypes" :key="type.value" style="margin-bottom: 8px;">
            <span>{{ type.label }}</span>
            <el-input-number
              v-model="examConfig.questionTypes[type.value]"
              :min="0"
              :max="10"
              style="margin-left: 12px;"
            />
          </div>
        </el-form-item>
        <!-- 难度 -->
        <el-form-item label="难度等级">
          <el-rate v-model="examConfig.difficulty" :max="5" />
        </el-form-item>
        <!-- 生成按钮 -->
        <el-form-item>
          <el-button type="primary" @click="handleGenerate" :loading="loading">
            生成考核
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 试卷预览与下载 -->
    <el-card v-if="examData" class="preview-card" style="margin-top: 24px;">
      <template #header>
        <div class="card-header">
          <span>试卷预览</span>
          <el-button type="success" @click="handleDownloadPDF">下载试卷(.pdf)</el-button>
          <el-button type="success" @click="handleDownloadWORD">下载试卷(.docx)</el-button>
        </div>
      </template>
      <div>
        <h3>{{ examData.title }}</h3>
        <div v-for="(q, idx) in examData.questions" :key="q.id" style="margin-bottom: 16px;">
          <div><b>Q{{ idx + 1 }} ({{ q.type }})：</b>{{ q.content }}</div>
          <div v-if="q.options">
            <div v-for="(opt, i) in q.options" :key="i">{{ String.fromCharCode(65 + i) }}. {{ opt }}</div>
          </div>
          <div><b>答案：</b>{{ q.answer }}</div>
          <div><b>解析：</b>{{ q.analysis }}</div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useExamStore } from '@/stores/exam'
import axios from 'axios'

const examStore = useExamStore()
const loading = ref(false)
const examData = ref(null)

const examConfig = ref({
  courseId: '',
  knowledgePoints: [],
  questionTypes: {
    single_choice: 0,
    multiple_choice: 0,
    true_false: 0,
    completion: 0,
    case_analysis: 0,
    programming: 0
  },
  difficulty: 3
})

const questionTypes = [
  { value: 'single_choice', label: '单选题' },
  { value: 'multiple_choice', label: '多选题' },
  { value: 'true_false', label: '判断题' },
  { value: 'completion', label: '填空题' },
  { value: 'case_analysis', label: '案例分析题' },
  { value: 'programming', label: '编程题' }
]

const courseOptions = computed(() => examStore.courseOptions)
const knowledgePointMap = computed(() => examStore.knowledgePointMap)
const currentKnowledgePoints = computed(() => {
  if (!examConfig.value.courseId) return []
  return knowledgePointMap.value[examConfig.value.courseId] || []
})

function onCourseChange() {
  examConfig.value.knowledgePoints = []
}

async function handleGenerate() {
  loading.value = true
  try {
    const token = localStorage.getItem('token')
    console.log('token:', token) // 调试用
    const res = await axios.post(
      '/api/v1/exams/generate',
      {
        course_id: examConfig.value.courseId,
        knowledge_points: examConfig.value.knowledgePoints,
        question_types: examConfig.value.questionTypes, // 包含题型和数量
        difficulty: examConfig.value.difficulty
      },
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )
    examData.value = res.data
  } catch (e) {
    examData.value = null
    window.$message?.error?.(e?.response?.data?.detail || '生成失败')
  }
  loading.value = false
}

async function handleDownloadPDF() {
  if (!examData.value) return
  const res = await axios.post(
    '/api/v1/exams/generate-pdf',
    examData.value,
    { responseType: 'blob' }
  )
  const blob = new Blob([res.data], { type: 'application/pdf' })
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${examData.value.title || 'exam'}.pdf`
  a.click()
  window.URL.revokeObjectURL(url)
}
async function handleDownloadWORD() {
  if (!examData.value) return
  const res = await axios.post(
    '/api/v1/exams/generate-word',
    examData.value,
    { responseType: 'blob' }
  )
  const blob = new Blob([res.data], { type: 'application/docx' })
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${examData.value.title || 'exam'}.docx`
  a.click()
  window.URL.revokeObjectURL(url)
}
</script>

<style scoped>
.exam-generator {
  padding: 20px;
}

.form-card {
  margin-bottom: 20px;
}

.preview-card {
  padding: 20px;
}

.preview-content {
  max-width: 800px;
  margin: 0 auto;
}
</style>