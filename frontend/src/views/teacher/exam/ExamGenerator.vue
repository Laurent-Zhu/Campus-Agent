<template>
  <div class="exam-generator">
    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <span>考核生成配置</span>
        </div>
      </template>

      <el-form :model="examConfig" label-width="120px">
        <!-- 课程选择 -->
        <el-form-item label="选择课程">
          <el-select v-model="examConfig.courseId" placeholder="请选择课程">
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
            placeholder="选择知识点"
          >
            <el-option
              v-for="point in knowledgePoints"
              :key="point"
              :label="point"
              :value="point"
            />
          </el-select>
        </el-form-item>

        <!-- 题型配置 -->
        <el-form-item label="题型配置">
          <div v-for="type in questionTypes" :key="type.value" class="question-type">
            <span class="type-label">{{ type.label }}</span>
            <el-input-number 
              v-model="examConfig.questionTypes[type.value]"
              :min="0"
              :max="10"
              @change="calculateTotal"
            />
            <span class="score-label">{{ type.score }}分/题</span>
          </div>
        </el-form-item>

        <!-- 难度设置 -->
        <el-form-item label="难度等级">
          <el-rate
            v-model="examConfig.difficulty"
            :max="5"
            show-score
          />
        </el-form-item>

        <!-- 总分展示 -->
        <el-form-item>
          <div class="total-info">
            <span>总题数: {{ totalQuestions }} 题</span>
            <span>总分: {{ totalScore }} 分</span>
          </div>
        </el-form-item>

        <!-- 生成按钮 -->
        <el-form-item>
          <el-button 
            type="primary" 
            :loading="generating"
            :disabled="!isValid"
            @click="handleGenerate"
          >
            生成试卷
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 预览区域 -->
    <el-card v-if="examData" class="preview-card">
      <template #header>
        <div class="card-header">
          <span>试卷预览</span>
          <div class="actions">
            <el-button type="primary" @click="handleSave">保存试卷</el-button>
            <el-button @click="handleExport">导出 Word</el-button>
          </div>
        </div>
      </template>

      <div class="exam-preview">
        <h1 class="exam-title">{{ examData.title }}</h1>
        <div class="exam-info">
          <span>总分: {{ examData.totalScore }}分</span>
          <span>时间: {{ examData.duration }}分钟</span>
        </div>

        <div v-for="(questions, type) in groupedQuestions" :key="type" class="question-section">
          <h2>{{ getQuestionTypeLabel(type) }}</h2>
          <div v-for="(q, index) in questions" :key="q.id" class="question-item">
            <div class="question-header">
              <span>第{{ index + 1 }}题 ({{ q.score }}分)</span>
              <el-button 
                type="primary" 
                link 
                @click="regenerateQuestion(type, index)"
              >
                重新生成
              </el-button>
            </div>
            <div class="question-content">{{ q.content }}</div>
            <div v-if="q.options" class="options">
              <div v-for="(opt, idx) in q.options" :key="idx" class="option">
                {{ ['A', 'B', 'C', 'D'][idx] }}. {{ opt }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useExamStore } from '@/stores/exam'
import { ElMessage } from 'element-plus'

const examStore = useExamStore()

// 状态定义
const generating = ref(false)
const examData = ref(null)
const examConfig = ref({
  courseId: '',
  knowledgePoints: [],
  questionTypes: {
    choice: 0,
    completion: 0,
    programming: 0
  },
  difficulty: 3
})

// 静态数据
const questionTypes = [
  { label: '选择题', value: 'choice', score: 5 },
  { label: '填空题', value: 'completion', score: 10 },
  { label: '编程题', value: 'programming', score: 20 }
]

// 计算属性
const totalQuestions = computed(() => {
  return Object.values(examConfig.value.questionTypes).reduce((sum, count) => sum + count, 0)
})

const totalScore = computed(() => {
  return Object.entries(examConfig.value.questionTypes).reduce((sum, [type, count]) => {
    const typeConfig = questionTypes.find(t => t.value === type)
    return sum + (typeConfig?.score || 0) * count
  }, 0)
})

const isValid = computed(() => {
  return examConfig.value.courseId && 
         examConfig.value.knowledgePoints.length > 0 && 
         totalQuestions.value > 0
})

const groupedQuestions = computed(() => {
  if (!examData.value) return {}
  return examData.value.questions.reduce((groups, q) => {
    if (!groups[q.type]) groups[q.type] = []
    groups[q.type].push(q)
    return groups
  }, {})
})

// 方法定义
const handleGenerate = async () => {
  if (!isValid.value) return
  
  generating.value = true
  try {
    const result = await examStore.generateExam(examConfig.value)
    examData.value = result
    ElMessage.success('试卷生成成功')
  } catch (error) {
    ElMessage.error(error.message || '生成失败')
  } finally {
    generating.value = false
  }
}

const handleSave = async () => {
  try {
    await examStore.saveExam(examData.value)
    ElMessage.success('保存成功')
  } catch (error) {
    ElMessage.error(error.message || '保存失败')
  }
}

const getQuestionTypeLabel = (type) => {
  return questionTypes.find(t => t.value === type)?.label || type
}
</script>

<style lang="scss" scoped>
.exam-generator {
  padding: 20px;
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 20px;
  
  .form-card {
    height: fit-content;
  }
  
  .question-type {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
    
    .type-label {
      width: 80px;
    }
    
    .score-label {
      margin-left: 10px;
      color: #909399;
      font-size: 14px;
    }
  }
  
  .total-info {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
    font-weight: bold;
  }
  
  .exam-preview {
    padding: 20px;
    
    .exam-title {
      text-align: center;
      margin-bottom: 20px;
    }
    
    .exam-info {
      text-align: center;
      margin-bottom: 30px;
      color: #606266;
      
      span {
        margin: 0 10px;
      }
    }
    
    .question-section {
      margin-bottom: 30px;
      
      h2 {
        border-bottom: 2px solid #409EFF;
        padding-bottom: 10px;
        margin-bottom: 20px;
      }
    }
    
    .question-item {
      margin-bottom: 20px;
      padding: 15px;
      border: 1px solid #EBEEF5;
      border-radius: 4px;
      
      .question-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
      }
      
      .options {
        margin-top: 10px;
        padding-left: 20px;
        
        .option {
          margin-bottom: 5px;
        }
      }
    }
  }
}
</style>