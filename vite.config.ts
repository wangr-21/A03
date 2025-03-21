import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'vue-vendor': ['vue', 'vue-router'],
          'ant-design': ['ant-design-vue'],
          echarts: ['echarts/core'],
          'echarts-components': ['echarts/charts', 'echarts/components', 'echarts/renderers'],
        },
      },
    },
    chunkSizeWarningLimit: 600,
  },
});
