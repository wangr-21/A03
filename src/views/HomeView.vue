<script setup lang="ts">
import { ref, reactive, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'
import * as echarts from 'echarts'
import type { EChartsType } from 'echarts'
import type { TabsPaneContext } from 'element-plus'

// 定义资源类型接口
interface Resource {
  id: number;
  title: string;
  cover: string;
  subject: string;
  grade: string;
  type: string;
}

// 定义图谱数据类型
interface GraphData {
  source: string;
  target: string;
  name: string;
}

// 图表实例
const overviewChart = ref<EChartsType | null>(null);
const knowledgeGraphChart = ref<EChartsType | null>(null);

// 数据
const overviewTimeRange = ref('month');
const searchContact = ref('');

// 图表初始化
const initCharts = () => {
  // 概览图表
  const overviewDom = document.getElementById('overviewChart');
  if (overviewDom) {
    overviewChart.value = echarts.init(overviewDom);
    const option = {
      title: {
        text: '学习资源访问趋势',
        left: 'center'
      },
      tooltip: {
        trigger: 'axis'
      },
      legend: {
        data: ['总访问量', '资源下载', '在线观看'],
        bottom: 0
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '10%',
        top: '15%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          name: '总访问量',
          type: 'line',
          data: [820, 932, 901, 934, 1290, 1330, 1320],
          smooth: true,
          lineStyle: {
            color: '#7353E5'
          }
        },
        {
          name: '资源下载',
          type: 'line',
          data: [320, 332, 301, 334, 390, 330, 320],
          smooth: true,
          lineStyle: {
            color: '#54D6FF'
          }
        },
        {
          name: '在线观看',
          type: 'line',
          data: [500, 600, 550, 600, 900, 1000, 1000],
          smooth: true,
          lineStyle: {
            color: '#FFB64D'
          }
        }
      ]
    };
    overviewChart.value?.setOption(option);
  }

  // 知识图谱
  const knowledgeDom = document.getElementById('knowledgeGraphChart');
  if (knowledgeDom) {
    knowledgeGraphChart.value = echarts.init(knowledgeDom);
    const option = {
      title: {
        text: '学科关联图',
        left: 'center'
      },
      tooltip: {
        formatter: function(params: echarts.DefaultLabelFormatterCallbackParams) {
          if ('dataType' in params && params.dataType === 'edge') {
            const data = params.data as GraphData;
            return `${params.name}: ${data.source} → ${data.target}`;
          }
          return String(params.name);
        }
      },
      legend: {
        data: ['核心学科', '自然科学', '应用科学'],
        bottom: 10,
        orient: 'horizontal',
        left: 'center'
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
            fontWeight: 'bold'
          },
          edgeSymbol: ['circle', 'arrow'],
          edgeSymbolSize: [4, 10],
          edgeLabel: {
            fontSize: 12,
            formatter: '{c}'
          },
          data: [
            { name: '数学', category: 0, itemStyle: { color: '#7353E5' } },
            { name: '物理', category: 1, itemStyle: { color: '#54D6FF' } },
            { name: '化学', category: 1, itemStyle: { color: '#FFB64D' } },
            { name: '生物', category: 1, itemStyle: { color: '#FF7A5A' } },
            { name: '计算机', category: 2, itemStyle: { color: '#FF5454' } }
          ],
          links: [
            { source: '数学', target: '物理', name: '基础' },
            { source: '数学', target: '化学', name: '基础' },
            { source: '数学', target: '计算机', name: '算法' },
            { source: '物理', target: '化学', name: '交叉' },
            { source: '生物', target: '化学', name: '交叉' }
          ],
          categories: [
            { name: '核心学科' }, 
            { name: '自然科学' }, 
            { name: '应用科学' }
          ],
          force: {
            repulsion: 200,
            edgeLength: 80,
            gravity: 0.1
          },
          emphasis: {
            focus: 'adjacency',
            lineStyle: {
              width: 4
            }
          }
        }
      ]
    };
    knowledgeGraphChart.value?.setOption(option);
  }
};

// 轮播数据
const carouselItems = [
  { id: 1, title: '优秀教学案例展示', description: '互动式历史课堂设计', image: '/src/assets/carousel1.jpg' },
  { id: 2, title: '学生创意作品欣赏', description: 'AI赋能美术创作', image: '/src/assets/carousel2.jpg' },
  { id: 3, title: '最新平台功能介绍', description: '学科星云知识图谱上线', image: '/src/assets/carousel3.jpg' }
];

// 热点数据
const hotspot = {
  title: '今日古诗推荐',
  content: '《望庐山瀑布》 - 李白\n日照香炉生紫烟，遥看瀑布挂前川。飞流直下三千尺，疑是银河落九天。'
};

// 资源库数据
const activeLibraryTab = ref('all');
const selectedSubject = ref('');
const selectedGrade = ref('');
const subjects = [
  '语文', '数学', '英语', '物理', '化学', '历史', '地理', '生物', '政治', '党建'
];
const grades = [
  '一年级', '二年级', '三年级', '四年级', '五年级', '六年级',
  '初一', '初二', '初三', '高一', '高二', '高三'
];
const allResources = ref<Resource[]>([]);
const resourcePageSize = ref(5);
const resourceCurrentPage = ref(1);
const resourcesLoading = ref(false);

// 联系人数据
const contacts = [
  { name: '王小明', title: '数学教师', avatar: '/src/assets/avatar1.jpg' },
  { name: '李晓华', title: '语文组长', avatar: '/src/assets/avatar2.jpg' },
  { name: '张三', title: '科学教师', avatar: '/src/assets/avatar3.jpg' }
];

// 过滤资源
const filteredResources = computed(() => {
  return allResources.value.filter(resource => {
    const typeMatch = activeLibraryTab.value === 'all' || resource.type === activeLibraryTab.value;
    const subjectMatch = !selectedSubject.value || resource.subject === selectedSubject.value;
    const gradeMatch = !selectedGrade.value || resource.grade === selectedGrade.value;
    return typeMatch && subjectMatch && gradeMatch;
  });
});

// 分页资源
const paginatedResources = computed(() => {
  const start = (resourceCurrentPage.value - 1) * resourcePageSize.value;
  const end = start + resourcePageSize.value;
  return filteredResources.value.slice(start, end);
});

// 方法
const viewHotspotDetail = () => {
  console.log('View hotspot detail');
};

const handleTabClick = (tab: TabsPaneContext) => {
  resourceCurrentPage.value = 1; // 切换标签时重置页码
};

const applyFilters = () => {
  resourceCurrentPage.value = 1;
  console.log('Filters applied:', activeLibraryTab.value, selectedSubject.value, selectedGrade.value);
};

const handleResourcePageChange = (page: number) => {
  resourceCurrentPage.value = page;
};

const fetchResources = () => {
  resourcesLoading.value = true;
  console.log('Fetching resources...');
  // 模拟 API 调用延迟
  setTimeout(() => {
    // 替换为实际 API 调用
    allResources.value = [
      { id: 1, title: '人教版语文七年级上册', cover: '/src/assets/resource_cover1.jpg', subject: '语文', grade: '初一', type: 'textbook' },
      { id: 2, title: '北师大版数学八年级下册', cover: '/src/assets/resource_cover2.jpg', subject: '数学', grade: '初二', type: 'textbook' },
      { id: 3, title: '《共产党宣言》导读', cover: '/src/assets/resource_cover3.jpg', subject: '党建', grade: '通用', type: 'party' },
      { id: 4, title: '外研社英语九年级全册', cover: '/src/assets/resource_cover4.jpg', subject: '英语', grade: '初三', type: 'textbook' },
      { id: 5, title: '党史故事100讲', cover: '/src/assets/resource_cover5.jpg', subject: '党建', grade: '通用', type: 'party' },
      { id: 6, title: '物理实验精选（高中）', cover: '/src/assets/resource_cover6.jpg', subject: '物理', grade: '高中', type: 'textbook' },
      { id: 7, title: '化学反应原理探究', cover: '/src/assets/resource_cover7.jpg', subject: '化学', grade: '高中', type: 'textbook' },
      { id: 8, title: '中国近代史纲要解读', cover: '/src/assets/resource_cover8.jpg', subject: '党建', grade: '通用', type: 'party' },
      { id: 9, title: '生物进化论浅析', cover: '/src/assets/resource_cover9.jpg', subject: '生物', grade: '高中', type: 'textbook' },
    ];
    resourcesLoading.value = false;
    console.log('Resources fetched.');
  }, 1000); // 模拟 1 秒延迟
};

const viewResource = (id: number) => {
  console.log('View resource:', id);
};

// 响应窗口大小变化
const handleResize = () => {
  overviewChart.value?.resize();
  knowledgeGraphChart.value?.resize();
};

// 生命周期钩子
onMounted(() => {
  fetchResources();
  // 确保DOM已经完全渲染后再初始化图表
  nextTick(() => {
    setTimeout(() => {
      initCharts();
      window.addEventListener('resize', handleResize);
    }, 300);
  });
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize);
  overviewChart.value?.dispose();
  knowledgeGraphChart.value?.dispose();
});
</script>

<template>
  <div class="home-container">
    <div class="page-header">
      <h1 class="page-title">启智学堂</h1>
    </div>
    
    <!-- 主要统计卡片区域 -->
    <div class="stats-cards">
      <el-card class="stats-card">
        <div class="stats-icon purple-bg">
          <el-icon><Files /></el-icon>
        </div>
        <div class="stats-info">
          <div class="stats-number">12,860</div>
          <div class="stats-label">总资源数</div>
        </div>
      </el-card>
      
      <el-card class="stats-card">
        <div class="stats-icon yellow-bg">
          <el-icon><DocumentAdd /></el-icon>
        </div>
        <div class="stats-info">
          <div class="stats-number">+ 152</div>
          <div class="stats-label">本周新增教案</div>
        </div>
      </el-card>
      
      <el-card class="stats-card">
        <div class="stats-icon orange-bg">
          <el-icon><UserFilled /></el-icon>
        </div>
        <div class="stats-info">
          <div class="stats-number">5,678</div>
          <div class="stats-label">活跃用户数</div>
        </div>
      </el-card>
      
      <el-card class="stats-card">
        <div class="stats-icon red-bg">
          <el-icon><Flag /></el-icon>
        </div>
        <div class="stats-info">
          <div class="stats-number">350</div>
          <div class="stats-label">党建资源数</div>
        </div>
      </el-card>
    </div>
    
    <!-- 概览图表区域 -->
    <el-card class="chart-card">
      <div class="card-header">
        <h3>概览</h3>
        <el-select v-model="overviewTimeRange" placeholder="Month" size="small">
          <el-option label="Month" value="month"></el-option>
          <el-option label="Week" value="week"></el-option>
          <el-option label="Year" value="year"></el-option>
        </el-select>
      </div>
      <div class="chart-container" id="overviewChart"></div>
    </el-card>
    
    <!-- 联系人区域 -->
    <el-card class="contacts-card">
      <div class="card-header">
        <h3>联系人(192)</h3>
        <el-input
          placeholder="搜索联系人"
          prefix-icon="Search"
          v-model="searchContact"
          size="small"
          class="contact-search"
        ></el-input>
      </div>
      
      <div class="contact-list">
        <div class="contact-item" v-for="(contact, index) in contacts" :key="index">
          <div class="contact-avatar">
            <img :src="contact.avatar" :alt="contact.name">
          </div>
          <div class="contact-info">
            <div class="contact-name">{{ contact.name }}</div>
            <div class="contact-title">{{ contact.title }}</div>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 流光展台区域 -->
    <el-row :gutter="20" class="showcase-area">
      <el-col :span="16"> <!-- 调整轮播图宽度 -->
        <el-card class="carousel-card">
          <el-carousel height="300px" arrow="always">
            <el-carousel-item v-for="item in carouselItems" :key="item.id">
              <img :src="item.image" class="carousel-image"/>
              <div class="carousel-caption">
                <h3>{{ item.title }}</h3>
                <p>{{ item.description }}</p>
              </div>
            </el-carousel-item>
          </el-carousel>
        </el-card>
      </el-col>
      <el-col :span="8"> <!-- 热点卡片 -->
        <el-card class="hotspot-card">
          <template #header>
            <div class="card-header">
              <h3><el-icon><DataLine /></el-icon> 动态学科热点</h3>
            </div>
          </template>
          <div class="hotspot-content">
            <h4>{{ hotspot.title }}</h4>
            <p>{{ hotspot.content }}</p>
            <el-button type="primary" text @click="viewHotspotDetail">查看详情</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 智汇文库区域 -->
    <el-card class="resource-library-card">
      <template #header>
        <div class="card-header">
          <h3><el-icon><Reading /></el-icon> 智汇文库</h3>
          <div class="library-filters">
            <el-tabs v-model="activeLibraryTab" @tab-click="handleTabClick">
              <el-tab-pane label="全部资源" name="all"></el-tab-pane>
              <el-tab-pane label="电子课本" name="textbook"></el-tab-pane>
              <el-tab-pane label="党建专题" name="party"></el-tab-pane>
            </el-tabs>
            <div class="filter-controls">
              <el-select v-model="selectedSubject" placeholder="选择学科" size="small" clearable @change="applyFilters">
                <el-option v-for="subject in subjects" :key="subject" :label="subject" :value="subject"></el-option>
              </el-select>
              <el-select v-model="selectedGrade" placeholder="选择年级" size="small" clearable @change="applyFilters">
                <el-option v-for="grade in grades" :key="grade" :label="grade" :value="grade"></el-option>
              </el-select>
            </div>
          </div>
        </div>
      </template>
      <div 
        class="resource-grid" 
        v-loading="resourcesLoading" 
        element-loading-text="加载资源中..."
      >
        <el-card 
          class="resource-card" 
          v-for="resource in paginatedResources" 
          :key="resource.id"
          shadow="hover"
        >
          <div class="resource-cover">
            <img :src="resource.cover" :alt="resource.title">
            <el-tag v-if="resource.type === 'party'" type="danger" class="party-tag">党建</el-tag>
          </div>
          <div class="resource-info">
            <h4>{{ resource.title }}</h4>
            <div class="resource-meta">
              <span>{{ resource.subject }}</span> | <span>{{ resource.grade }}</span>
            </div>
            <el-button text type="primary" @click="viewResource(resource.id)">开始阅读</el-button>
          </div>
        </el-card>
      </div>
      <div class="pagination" v-if="filteredResources.length > 0">
         <el-pagination 
           background 
           layout="prev, pager, next" 
           :total="filteredResources.length" 
           :page-size="resourcePageSize" 
           v-model:current-page="resourceCurrentPage"
           @current-change="handleResourcePageChange"
         ></el-pagination>
      </div>
      <el-empty v-if="!resourcesLoading && filteredResources.length === 0" description="暂无匹配资源"></el-empty>
    </el-card>

    <!-- 学科星云区域 (暂时占位) -->
    <el-card class="knowledge-graph-card">
        <template #header>
          <div class="card-header">
            <h3><el-icon><Share /></el-icon> 学科星云</h3>
          </div>
        </template>
        <div class="chart-container" id="knowledgeGraphChart"></div>
    </el-card>
  </div>
</template>

<style scoped>
.home-container {
  padding: 20px;
  min-height: 100%;
}

.page-header {
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

/* 响应式布局调整 */
@media (max-width: 1399px) {
  .stats-cards {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
  }
}

@media (max-width: 768px) {
  .stats-cards {
    grid-template-columns: 1fr;
    gap: 10px;
  }
}

.stats-card {
  display: flex;
  align-items: center;
  padding: 20px;
  transition: transform 0.3s, box-shadow 0.3s;
  border-radius: 8px;
  overflow: hidden;
}

.stats-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.stats-icon {
  width: 60px;
  height: 60px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20px;
}

.stats-icon .el-icon {
  font-size: 28px;
  color: white;
}

.purple-bg {
  background-color: #7353E5;
}

.yellow-bg {
  background-color: #FFB64D;
}

.orange-bg {
  background-color: #FF7A5A;
}

.red-bg {
  background-color: #FF5454;
}

.stats-info {
  flex: 1;
}

.stats-number {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.stats-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

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

.card-header h3 .el-icon {
  color: #7353E5;
}

.chart-container {
  height: 350px;
  width: 100%;
  padding: 0 10px;
}

.contacts-card {
  margin-bottom: 30px;
  border-radius: 8px;
}

.contact-search {
  width: 250px;
}

.contact-list {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  padding: 10px 20px;
}

.contact-item {
  display: flex;
  align-items: center;
  padding: 10px;
  border-radius: 8px;
  background-color: #f9f9f9;
  width: calc(33.33% - 10px);
  transition: all 0.3s ease;
}

.contact-item:hover {
  background-color: #f0f0f0;
  transform: translateY(-2px);
}

@media (max-width: 1199px) {
  .contact-item {
    width: calc(50% - 10px);
  }
}

@media (max-width: 768px) {
  .contact-item {
    width: 100%;
  }
  
  .contact-search {
    width: 100%;
  }
}

.contact-avatar {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 15px;
}

.contact-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.contact-name {
  font-weight: bold;
  color: #333;
}

.contact-title {
  font-size: 12px;
  color: #909399;
  margin-top: 3px;
}

.showcase-area {
  margin-bottom: 30px;
}

/* 响应式调整展示区域 */
@media (max-width: 991px) {
  .el-col[class*=el-col-] {
    width: 100%;
    margin-bottom: 20px;
  }
}

.carousel-card {
  height: 360px;
  border-radius: 8px;
  overflow: hidden;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.carousel-caption {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.5);
  padding: 15px;
}

.carousel-caption h3 {
  font-size: 20px;
  font-weight: bold;
  color: white;
}

.carousel-caption p {
  font-size: 14px;
  color: white;
  margin-top: 5px;
}

.hotspot-card {
  height: 360px;
  display: flex;
  flex-direction: column;
  border-radius: 8px;
  overflow: hidden;
}

.hotspot-content {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.hotspot-content h4 {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin-bottom: 15px;
}

.hotspot-content p {
  font-size: 16px;
  color: #606266;
  line-height: 1.6;
  white-space: pre-line;
  flex: 1;
}

.hotspot-content .el-button {
  margin-top: 15px;
  align-self: flex-start;
}

.resource-library-card {
  margin-bottom: 30px;
  border-radius: 8px;
  overflow: hidden;
}

.library-filters {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: 15px;
}

/* 响应式调整过滤器 */
@media (max-width: 768px) {
  .library-filters {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .filter-controls {
    margin-top: 10px;
    width: 100%;
  }
  
  .filter-controls .el-select {
    width: 100%;
    margin-bottom: 10px;
  }
}

.filter-controls {
  display: flex;
  gap: 15px;
}

.resource-grid {
  display: flex;
  flex-direction: column;
  gap: 15px;
  min-height: 200px;
  padding: 0 20px 20px;
}

.resource-card {
  display: flex;
  align-items: center;
  padding: 15px;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  transition: all 0.3s ease;
  background-color: #fff;
}

.resource-card:hover {
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}

/* 资源卡片响应式调整 */
@media (max-width: 480px) {
  .resource-card {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .resource-cover {
    width: 100%;
    height: 200px;
    margin-right: 0;
    margin-bottom: 15px;
  }
}

.resource-cover {
  width: 120px;
  height: 160px;
  overflow: hidden;
  border-radius: 6px;
  margin-right: 20px;
  position: relative;
}

.resource-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.party-tag {
  position: absolute;
  right: 5px;
  top: 5px;
}

.resource-info {
  flex: 1;
}

.resource-info h4 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.resource-meta {
  font-size: 14px;
  color: #909399;
  margin-bottom: 10px;
}

.resource-info .el-button {
  margin-top: 5px;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.knowledge-graph-card {
  margin-bottom: 30px;
  border-radius: 8px;
  overflow: hidden;
}

/* ECharts图表容器样式 */
#overviewChart, #knowledgeGraphChart {
  width: 100%;
  height: 100%;
}

/* 知识图谱图表高度 */
.knowledge-graph-card .chart-container {
  height: 450px; /* 更大的高度以便更好地展示图谱 */
}
</style>
