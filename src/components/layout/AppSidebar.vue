<script setup lang="ts">
defineProps({
  isMobile: {
    type: Boolean,
    default: false,
  },
});

const collapsed = defineModel<boolean>('collapsed');

const emit = defineEmits<{
  'toggle-sidebar': [];
  'goto-workshop': [];
}>();

const handleStartButtonClick = () => {
  collapsed.value = true;
  emit('goto-workshop');
};
</script>

<template>
  <div class="sidebar">
    <div class="logo-container">
      <img alt="Logo" class="logo" src="/src/assets/icons/logo.svg" />
      <span class="app-name" v-if="!collapsed">智教通平台</span>
    </div>

    <!-- 菜单导航 -->
    <el-menu
      class="sidebar-menu"
      background-color="#7353E5"
      text-color="#ffffff"
      active-text-color="#ffffff"
      :default-active="$route.path"
      :collapse="collapsed"
      router
    >
      <el-menu-item index="/" route="/">
        <el-icon><Grid /></el-icon>
        <template #title>启智学堂</template>
      </el-menu-item>
      <el-menu-item index="/workshop" route="/workshop">
        <el-icon><ChatDotRound /></el-icon>
        <template #title>智课工坊</template>
      </el-menu-item>
      <el-menu-item index="/lab" route="/lab">
        <el-icon><PictureFilled /></el-icon>
        <template #title>幻画实验室</template>
      </el-menu-item>
      <el-menu-item index="/lighthouse" route="/lighthouse">
        <el-icon><User /></el-icon>
        <template #title>学海灯塔</template>
      </el-menu-item>
      <el-menu-item index="/community" route="/community">
        <el-icon><PriceTag /></el-icon>
        <template #title>师韵星盟</template>
      </el-menu-item>
    </el-menu>

    <!-- 底部欢迎语 -->
    <div class="welcome-text" v-if="!collapsed">
      <p>欢迎来到智教通平台！</p>
      <p class="sub-text">AI赋能教学，引领未来教育</p>
      <el-button type="primary" class="open-btn" @click="handleStartButtonClick"
        >现在开始！</el-button
      >
    </div>

    <!-- 折叠按钮 -->
    <div class="sidebar-collapse-btn" @click="emit('toggle-sidebar')">
      <el-icon v-if="collapsed"><ArrowRight /></el-icon>
      <el-icon v-else><ArrowLeft /></el-icon>
    </div>
  </div>
</template>

<style scoped>
.sidebar {
  width: 260px;
  background: linear-gradient(to bottom, #7353e5, #6b42e8);
  color: white;
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
  transition: all 0.3s ease;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  flex-shrink: 0;
  margin: 0;
  padding: 0;
}

.logo-container {
  display: flex;
  align-items: center;
  padding: 1.25rem;
  height: 64px;
}

.logo {
  width: 32px;
  height: 32px;
}

.app-name {
  font-size: 1.375rem;
  font-weight: bold;
  margin-left: 0.625rem;
  white-space: nowrap;
}

.welcome-text {
  margin-top: auto;
  padding: 1.25rem;
  text-align: center;
}

.sub-text {
  font-size: 0.75rem;
  margin-top: 0.3125rem;
  opacity: 0.7;
}

.open-btn {
  width: 100%;
  margin-top: 0.9375rem;
  background-color: #54d6ff;
  border: none;
}

.sidebar-collapse-btn {
  position: absolute;
  right: -12px;
  top: 70px;
  width: 24px;
  height: 24px;
  background-color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.12);
  z-index: 2;
}

.sidebar-collapse-btn .el-icon {
  font-size: 12px;
  color: #909399;
}
</style>
