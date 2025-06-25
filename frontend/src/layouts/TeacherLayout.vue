<template>
  <el-container class="layout-container">
    <el-aside width="200px">
      <el-menu
        :router="true"
        class="el-menu-vertical"
      >
        <el-menu-item index="/teacher/exam">
          <el-icon><Document /></el-icon>
          <span>考核管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    
    <el-container>
      <el-header>
        <div class="header-content">
          <h2>教师工作台</h2>
        </div>
      </el-header>
      
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { ElMessageBox } from 'element-plus';
import {
  Document,
} from '@element-plus/icons-vue';

const router = useRouter();
const route = useRoute();
const isCollapse = ref(false);

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确认退出系统吗？', '提示', {
      type: 'warning'
    });
    router.push('/login');
  } catch {
    // 取消退出
  }
};
</script>

<style lang="scss" scoped>
.layout-container {
  height: 100vh;
}

.el-aside {
  background-color: #304156;
  transition: width 0.3s;
  
  .logo {
    height: 60px;
    display: flex;
    align-items: center;
    padding: 0 20px;
    color: white;
    
    img {
      width: 32px;
      height: 32px;
    }
    
    span {
      margin-left: 12px;
      font-size: 16px;
      font-weight: bold;
    }
  }
}

.el-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  background-color: white;
  border-bottom: 1px solid #dcdfe6;
}
</style>