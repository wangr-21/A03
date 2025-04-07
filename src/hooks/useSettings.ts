import { ref, watch, type Ref } from 'vue';

export function useSettings(showNotificationDropdown: Ref<boolean>) {
  const showSettingsDropdown = ref(false);

  const toggleSettingsDropdown = () => {
    // 关闭通知下拉菜单（如果打开）
    showNotificationDropdown.value = false;
    showSettingsDropdown.value = !showSettingsDropdown.value;
  };

  const closeSettingsDropdown = () => {
    showSettingsDropdown.value = false;
  };

  watch(
    () => showNotificationDropdown.value,
    (newVal) => {
      if (newVal) showSettingsDropdown.value = false;
    },
  );

  return {
    showSettingsDropdown,
    toggleSettingsDropdown,
    closeSettingsDropdown,
  };
}
