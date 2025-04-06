<script setup lang="ts">
import { RouterView } from 'vue-router';
import MainLayout from './layouts/MainLayout.vue';
</script>

<template>
  <MainLayout>
    <RouterView v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </RouterView>
  </MainLayout>
</template>

<style>
@import '@/assets/styles/global.css';
@import '@/assets/styles/element-override.css';
</style>
