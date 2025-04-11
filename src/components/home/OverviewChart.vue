<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue';
import { use, init, type EChartsType } from 'echarts/core';
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
} from 'echarts/components';
import { LineChart } from 'echarts/charts';
import { UniversalTransition } from 'echarts/features';
import { CanvasRenderer } from 'echarts/renderers';

// 注册必需的组件
use([
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  LineChart,
  CanvasRenderer,
  UniversalTransition,
]);

const overviewChart = ref<EChartsType | null>(null);
const overviewTimeRange = ref<string>('month');

// 图表初始化
const initChart = (): void => {
  const chartDom = document.getElementById('overviewChart');
  if (!chartDom) return;

  overviewChart.value = init(chartDom);
  updateChartData();
};

// 更新图表数据
const updateChartData = (): void => {
  if (!overviewChart.value) return;

  // 根据选择的时间范围生成不同的数据
  let xAxisData: string[] = [];
  let totalAccessData: number[] = [];
  let resourceDownloadData: number[] = [];
  let onlineViewData: number[] = [];

  if (overviewTimeRange.value === 'week') {
    xAxisData = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'];
    totalAccessData = [820, 932, 901, 934, 1290, 1330, 1320];
    resourceDownloadData = [320, 332, 301, 334, 390, 330, 320];
    onlineViewData = [500, 600, 550, 600, 900, 1000, 1000];
  } else if (overviewTimeRange.value === 'month') {
    xAxisData = Array.from({ length: 30 }, (_, i) => `${i + 1}日`);
    // 生成30天的随机数据
    totalAccessData = Array.from({ length: 30 }, () => Math.floor(Math.random() * 1000) + 800);
    resourceDownloadData = Array.from({ length: 30 }, () => Math.floor(Math.random() * 400) + 300);
    onlineViewData = Array.from({ length: 30 }, () => Math.floor(Math.random() * 600) + 400);
  } else if (overviewTimeRange.value === 'year') {
    xAxisData = [
      '1月',
      '2月',
      '3月',
      '4月',
      '5月',
      '6月',
      '7月',
      '8月',
      '9月',
      '10月',
      '11月',
      '12月',
    ];
    totalAccessData = [2200, 1820, 1910, 2340, 2900, 3300, 3100, 2500, 2800, 3200, 3590, 3800];
    resourceDownloadData = [1200, 1100, 1240, 1130, 1400, 1800, 1700, 1500, 1600, 1800, 1900, 2000];
    onlineViewData = [1000, 720, 670, 1210, 1500, 1500, 1400, 1000, 1200, 1400, 1690, 1800];
  }

  const option = {
    title: {
      text: '学习资源访问趋势',
      left: 'center',
    },
    tooltip: {
      trigger: 'axis',
    },
    legend: {
      data: ['总访问量', '资源下载', '在线观看'],
      bottom: 0,
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '10%',
      top: '15%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: xAxisData,
    },
    yAxis: {
      type: 'value',
    },
    series: [
      {
        name: '总访问量',
        type: 'line',
        data: totalAccessData,
        smooth: true,
        lineStyle: {
          color: '#7353E5',
        },
      },
      {
        name: '资源下载',
        type: 'line',
        data: resourceDownloadData,
        smooth: true,
        lineStyle: {
          color: '#54D6FF',
        },
      },
      {
        name: '在线观看',
        type: 'line',
        data: onlineViewData,
        smooth: true,
        lineStyle: {
          color: '#FFB64D',
        },
      },
    ],
  };

  overviewChart.value.setOption(option);
};

// 处理时间范围变化
const handleTimeRangeChange = () => {
  updateChartData();
};

// 响应窗口大小变化
const handleResize = (): void => {
  overviewChart.value?.resize();
};

// 生命周期
onMounted(() => {
  nextTick(() => {
    setTimeout(() => {
      initChart();
      window.addEventListener('resize', handleResize);
    }, 300);
  });
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize);
  overviewChart.value?.dispose();
});
</script>

<template>
  <el-card class="chart-card">
    <div class="card-header">
      <h3>概览</h3>
      <el-select
        v-model="overviewTimeRange"
        placeholder="Month"
        size="small"
        @change="handleTimeRangeChange"
        style="width: 10%"
      >
        <el-option label="月" value="month"></el-option>
        <el-option label="周" value="week"></el-option>
        <el-option label="年" value="year"></el-option>
      </el-select>
    </div>
    <div class="chart-container" id="overviewChart"></div>
  </el-card>
</template>

<style scoped>
.chart-card {
  margin-bottom: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding: 15px 20px 0;
}

.card-header h3 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.chart-container {
  height: 350px;
  width: 100%;
  padding: 0 10px;
}

/* ECharts图表容器样式 */
#overviewChart {
  width: 100%;
  height: 100%;
}
</style>
