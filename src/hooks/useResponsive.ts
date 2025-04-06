import { ref, onMounted, onBeforeUnmount } from 'vue';

export function useResponsive() {
  const sidebarCollapsed = ref(false);
  const isMobile = ref(false);

  const toggleSidebar = () => {
    sidebarCollapsed.value = !sidebarCollapsed.value;
  };

  const handleResize = () => {
    isMobile.value = window.innerWidth < 768;
    // 在移动设备上自动折叠侧边栏
    if (isMobile.value) {
      sidebarCollapsed.value = true;
    } else {
      // 在桌面端默认展开侧边栏
      sidebarCollapsed.value = false;
    }
  };

  onMounted(() => {
    handleResize(); // 初始检查
    window.addEventListener('resize', handleResize);
  });

  onBeforeUnmount(() => {
    window.removeEventListener('resize', handleResize);
  });

  return { sidebarCollapsed, isMobile, toggleSidebar };
}
