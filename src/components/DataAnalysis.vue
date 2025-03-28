<template>
  <el-container style="padding: 24px">
    <el-main>
      <el-loading :value="loading">
        <el-row :gutter="24">
          <el-col :span="6" v-for="(data, index) in analysisData" :key="index">
            <el-card>
              <div class="statistic-item">
                <el-icon class="statistic-icon" :style="{ color: data.color }">
                  <component :is="data.icon" />
                </el-icon>
                <div class="statistic-content">
                  <div class="statistic-title">{{ data.title }}</div>
                  <div class="statistic-value" :style="{ color: data.color }">
                    {{ data.value }}{{ data.prefix }}
                  </div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <el-row :gutter="16" style="margin-top: 24px">
          <el-col :span="12">
            <el-card header="学习进度分析">
              <div ref="chartRef1" style="height: 400px"></div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card header="学习时长分布">
              <div ref="chartRef2" style="height: 400px"></div>
            </el-card>
          </el-col>
        </el-row>
      </el-loading>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, nextTick } from 'vue';
import { ElMessage } from 'element-plus';

// 按需导入ECharts核心模块
import * as echarts from 'echarts/core';
import { BarChart, BarSeriesOption, RadarChart, RadarSeriesOption } from 'echarts/charts';
import {
  TitleComponent,
  TitleComponentOption,
  TooltipComponent,
  TooltipComponentOption,
  GridComponent,
  GridComponentOption,
  LegendComponent,
} from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';

// 声明组合图表类型
type ECOption = echarts.ComposeOption<
  | BarSeriesOption
  | RadarSeriesOption
  | TitleComponentOption
  | TooltipComponentOption
  | GridComponentOption
>;

// 注册必要的组件
echarts.use([
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  BarChart,
  RadarChart,
  CanvasRenderer,
]);

const loading = ref(true);
const chartRef1 = ref<HTMLElement | null>(null);
const chartRef2 = ref<HTMLElement | null>(null);

const analysisData = reactive([
  {
    title: '学习能力评估',
    value: 0,
    icon: 'User',
    prefix: '分',
    color: '#409EFF',
  },
  {
    title: '知识点掌握度',
    value: 0,
    icon: 'Reading',
    prefix: '%',
    color: '#67C23A',
  },
  {
    title: '完成任务数',
    value: 0,
    icon: 'Select',
    prefix: '个',
    color: '#8E44AD',
  },
  {
    title: '学习进度',
    value: 0,
    icon: 'Histogram',
    prefix: '%',
    color: '#E6A23C',
  },
] as {
  title: string;
  value: number;
  icon: string;
  prefix: string;
  color: string;
}[]);

const fetchAnalysisData = async () => {
  try {
    // 模拟API调用
    setTimeout(() => {
      // 更新分析数据
      analysisData[0].value = 85;
      analysisData[1].value = 78;
      analysisData[2].value = 12;
      analysisData[3].value = 65;

      loading.value = false;
      initCharts();
    }, 1000);
  } catch (error) {
    ElMessage.error('获取学情分析数据失败，请重试');
    console.error('获取分析数据错误:', error);
    loading.value = false;
  }
};

const initCharts = async () => {
  await nextTick();

  if (chartRef1.value) {
    const chart1 = echarts.init(chartRef1.value);
    const option: ECOption = {
      title: {
        text: '知识点掌握情况',
      },
      tooltip: {},
      radar: {
        indicator: [
          { name: '语言知识', max: 100 },
          { name: '文学常识', max: 100 },
          { name: '阅读能力', max: 100 },
          { name: '写作能力', max: 100 },
          { name: '口语表达', max: 100 },
        ],
      },
      series: [
        {
          type: 'radar',
          data: [
            {
              value: [80, 75, 85, 70, 78],
              name: '班级平均水平',
            },
          ],
        },
      ],
    };
    chart1.setOption(option);

    // 添加窗口大小变化时的自适应处理
    window.addEventListener('resize', () => {
      chart1.resize();
    });
  }

  if (chartRef2.value) {
    const chart2 = echarts.init(chartRef2.value);
    const option: ECOption = {
      title: {
        text: '每周学习时长分布',
      },
      xAxis: {
        type: 'category',
        data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
      },
      yAxis: {
        type: 'value',
      },
      series: [
        {
          data: [30, 35, 40, 38, 42, 25, 20],
          type: 'bar',
        },
      ],
    };
    chart2.setOption(option);
  }
};

onMounted(() => {
  fetchAnalysisData();
});
</script>

<style scoped>
.statistic-item {
  display: flex;
  align-items: center;
}

.statistic-icon {
  font-size: 24px;
  margin-right: 12px;
}

.statistic-content {
  flex: 1;
}

.statistic-title {
  font-size: 14px;
  color: #999;
  margin-bottom: 4px;
}

.statistic-value {
  font-size: 24px;
  font-weight: bold;
}
</style>
