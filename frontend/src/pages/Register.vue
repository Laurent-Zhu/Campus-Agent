<template>
  <div class="register-container">
    <el-card class="register-card">
      <h2>注册</h2>
      <el-form :model="form" @submit.prevent="handleRegister">
        <el-form-item label="用户名">
          <el-input v-model="form.username" autocomplete="username" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" autocomplete="email" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" autocomplete="new-password" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleRegister" :loading="loading">注册</el-button>
        </el-form-item>
      </el-form>
      <div style="margin-top: 12px;">
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
  password: ''
})
const loading = ref(false)

async function handleRegister() {
  loading.value = true
  try {
    await axios.post('/api/v1/auth/register', {
      username: form.value.username,
      email: form.value.email,
      password: form.value.password
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
}
.register-card {
  width: 350px;
}
</style>
