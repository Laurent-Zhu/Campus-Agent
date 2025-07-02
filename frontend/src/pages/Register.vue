<template>
  <div class="register-container">
    <el-card class="register-card">
      <h2 class="register-title">注册</h2>
      <el-form :model="form" @submit.prevent="handleRegister" label-position="top">
        <el-form-item label="用户名">
          <el-input v-model="form.username" autocomplete="username" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" autocomplete="email" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input
            v-model="form.password"
            type="password"
            autocomplete="new-password"
          />
        </el-form-item>
        <el-form-item label="身份">
          <el-select v-model="form.role" placeholder="请选择身份">
            <el-option label="学生" value="student"></el-option>
            <el-option label="教师" value="teacher"></el-option>
            <el-option label="管理员" value="admin"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button
            style="background-color: #2ea44f; border-color: #2ea44f; color: white; width: 100%"
            @click="handleRegister"
            :loading="loading"
          >
            注册
          </el-button>
        </el-form-item>
      </el-form>
      <div class="login-link">
        已有账号？<router-link to="/login">去登录</router-link>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = ref({
  username: '',
  email: '',
  password: '',
  role: '' // 添加身份字段
})
const loading = ref(false)

async function handleRegister() {
  loading.value = true
  try {
    await axios.post('/api/v1/auth/register', {
      username: form.value.username,
      email: form.value.email,
      password: form.value.password,
      role: form.value.role // 将身份传递到后端
    })
    window.$message?.success?.('注册成功，请登录')
    router.push('/login')
  } catch (e) {
    window.$message?.error?.(e?.response?.data?.detail || '注册失败')
  }
  loading.value = false
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f6f8fa;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue',
    Arial, 'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
    'Noto Color Emoji';
}

.register-card {
  width: 360px;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  border: 1px solid #d0d7de;
  background-color: #ffffff;
}

.register-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #24292f;
  text-align: center;
}

.login-link {
  margin-top: 16px;
  font-size: 14px;
  color: #57606a;
  text-align: center;
}

.login-link a {
  color: #0969da;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
