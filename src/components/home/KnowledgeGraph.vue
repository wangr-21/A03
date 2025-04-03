<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue';
import * as echarts from 'echarts';
import type { EChartsType } from 'echarts';

// 定义图谱数据类型
interface GraphData {
  source: string;
  target: string;
  name: string;
}

const knowledgeGraphChart = ref<EChartsType | null>(null);

// 图表初始化
const initChart = (): void => {
  const knowledgeDom = document.getElementById('knowledgeGraphChart');
  if (!knowledgeDom) return;

  knowledgeGraphChart.value = echarts.init(knowledgeDom);
  const option = {
    title: {
      text: '学科关联图',
      left: 'center',
    },
    tooltip: {
      formatter: function (params: echarts.DefaultLabelFormatterCallbackParams) {
        if ('dataType' in params && params.dataType === 'edge') {
          const data = params.data as GraphData;
          return `${params.name}: ${data.source} → ${data.target}`;
        }
        return String(params.name);
      },
    },
    legend: {
      data: ['核心学科', '自然科学', '应用科学'],
      bottom: 10,
      orient: 'horizontal',
      left: 'center',
    },
    series: [
      {
        type: 'graph',
        layout: 'force',
        symbolSize: 45,
        roam: true,
        label: {
          show: true,
          color: '#333',
          fontWeight: 'bold',
        },
        edgeSymbol: ['circle', 'arrow'],
        edgeSymbolSize: [4, 10],
        edgeLabel: {
          fontSize: 12,
          formatter: '{c}',
        },
        data: [
          { name: '数学', category: 0, itemStyle: { color: '#7353E5' } },
          { name: '物理', category: 1, itemStyle: { color: '#54D6FF' } },
          { name: '化学', category: 1, itemStyle: { color: '#FFB64D' } },
          { name: '生物', category: 1, itemStyle: { color: '#FF7A5A' } },
          { name: '计算机', category: 2, itemStyle: { color: '#FF5454' } },
        ],
        links: [
          { source: '数学', target: '物理', name: '基础' },
          { source: '数学', target: '化学', name: '基础' },
          { source: '数学', target: '计算机', name: '算法' },
          { source: '物理', target: '化学', name: '交叉' },
          { source: '生物', target: '化学', name: '交叉' },
        ],
        categories: [{ name: '核心学科' }, { name: '自然科学' }, { name: '应用科学' }],
        force: {
          repulsion: 200,
          edgeLength: 80,
          gravity: 0.1,
        },
        emphasis: {
          focus: 'adjacency',
          lineStyle: {
            width: 4,
          },
        },
      },
    ],
  };

  knowledgeGraphChart.value.setOption(option);
};

// 响应窗口大小变化
const handleResize = (): void => {
  knowledgeGraphChart.value?.resize();
};

// 生命周期钩子
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
  knowledgeGraphChart.value?.dispose();
});
</script>

<template>
  <el-card class="knowledge-graph-card">
    <template #header>
      <div class="card-header">
        <h3>
          <el-icon><Share /></el-icon> 学科星云
        </h3>
      </div>
    </template>
    <div class="chart-container" id="knowledgeGraphChart"></div>
  </el-card>
</template>

<style scoped>
.knowledge-graph-card {
  margin-bottom: 30px;
  border-radius: 8px;
  overflow: hidden;
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

.card-header h3 .el-icon {
  color: #7353e5;
}

.chart-container {
  height: 450px;
  width: 100%;
  padding: 0 10px;
}

/* ECharts图表容器样式 */
#knowledgeGraphChart {
  width: 100%;
  height: 100%;
}
</style>
