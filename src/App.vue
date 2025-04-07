<script setup lang="ts">
import { RouterView, useRoute, useRouter } from 'vue-router';
import { computed } from 'vue';
import MainLayout from './layouts/MainLayout.vue';

const router = useRouter();
const route = useRoute();
const hideLayout = computed(() => route.meta.hideLayout);
</script>

<template>
  <MainLayout v-if="!hideLayout" @router-goto="router.push">
    <RouterView v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </RouterView>
  </MainLayout>
  <RouterView v-else v-slot="{ Component }">
    <transition name="fade" mode="out-in">
      <component :is="Component" />
    </transition>
  </RouterView>
</template>

<style>
@import '@/assets/styles/global.css';
@import '@/assets/styles/element-override.css';

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
