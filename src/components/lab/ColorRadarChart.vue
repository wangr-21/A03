<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import * as echarts from 'echarts';
import type { EChartsType } from 'echarts';

const props = defineProps<{
  chartData: number[];
}>();

const chartRef = ref<HTMLElement | null>(null);
let chartInstance: EChartsType | null = null;

const initChart = () => {
  if (!chartRef.value) return;

  if (chartInstance) chartInstance.dispose();

  chartInstance = echarts.init(chartRef.value);
  const option = {
    tooltip: { trigger: 'item' },
    radar: {
      indicator: [
        { name: '暖度', max: 100 },
        { name: '亮度', max: 100 },
        { name: '对比度', max: 100 },
        { name: '饱和度', max: 100 },
        { name: '和谐度', max: 100 },
      ],
    },
    series: [
      {
        name: '色彩分析',
        type: 'radar',
        data: [{ value: props.chartData, name: '分析结果' }],
      },
    ],
  };
  chartInstance.setOption(option);
};

// 监听窗口变化，重新渲染图表
window.addEventListener('resize', () => {
  chartInstance?.resize();
});

// 监听数据变化
watch(
  () => props.chartData,
  () => {
    initChart();
  },
  { deep: true },
);

onMounted(() => {
  initChart();
});
</script>

<template>
  <div ref="chartRef" style="height: 300px"></div>
</template>
