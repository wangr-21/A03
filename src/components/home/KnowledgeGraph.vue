<script setup lang="ts">
import { ref, computed } from 'vue';
import { ElSelect, ElOption, ElDialog } from 'element-plus';

// 直接导入图片 (这是Vite支持的方式)
import artLiterature from '@/assets/datawithmix/art_literature.png';
import artMath from '@/assets/datawithmix/art_math.png';
import artHistory from '@/assets/datawithmix/art_history.png';
import artGeography from '@/assets/datawithmix/art_geography.png';
import artBiology from '@/assets/datawithmix/art_biology.png';

// 定义学科组合类型
type DisciplinePair = '美术+语文' | '美术+数学' | '美术+历史' | '美术+地理' | '美术+生物';

// 热区形状和坐标 (使用绝对定位 div，定义左上角和宽高)
interface Hotspot {
  id: string; // 唯一标识
  infoKey: string; // 用于查找详细信息的键
  style: {
    // CSS 样式
    top: string; // '10%' or '50px'
    left: string;
    width: string;
    height: string;
  };
}

// 详细信息结构
interface HotspotDetail {
  title: string;
  description: string;
  examples?: string[];
  resources?: string[];
}

// 图片资源映射
const imageMap = {
  '美术+语文': artLiterature,
  '美术+数学': artMath,
  '美术+历史': artHistory,
  '美术+地理': artGeography,
  '美术+生物': artBiology,
};

// 各图片的热区数据 (示例坐标，需要根据实际图片调整)
const imageHotspots: Record<DisciplinePair, Hotspot[]> = {
  '美术+语文': [
    {
      id: 'my_1',
      infoKey: '国画',
      style: { top: '15%', left: '10%', width: '20%', height: '15%' },
    },
    {
      id: 'my_2',
      infoKey: '诗词',
      style: { top: '35%', left: '70%', width: '18%', height: '12%' },
    },
    {
      id: 'my_3',
      infoKey: '书法',
      style: { top: '60%', left: '25%', width: '15%', height: '20%' },
    },
    // ... 可以添加更多热区
  ],
  '美术+数学': [], // 待添加
  '美术+历史': [], // 待添加
  '美术+地理': [], // 待添加
  '美术+生物': [], // 待添加
};

// 热区对应的详细信息 (复用之前的结构)
const hotspotDetails: Record<string, HotspotDetail> = {
  国画: {
    title: '国画艺术',
    description: '中国传统绘画艺术，以水墨为主要表现手法，强调意境和笔墨情趣。',
    examples: [
      '山水画：表现自然景观，如《千里江山图》',
      '花鸟画：描绘花卉鸟兽，如《百鸟朝凤》',
      '人物画：刻画人物形象，如《清明上河图》',
    ],
    resources: ['国画基础教程', '水墨画技法', '中国画史'],
  },
  诗词: {
    title: '诗词艺术',
    description: '中国古典文学的重要形式，通过韵律和意象表达情感和思想。',
    examples: [
      '山水诗：如王维的《山居秋暝》',
      '田园诗：如陶渊明的《归园田居》',
      '抒情诗：如李白的《静夜思》',
    ],
    resources: ['诗词鉴赏', '唐诗三百首', '宋词选读'],
  },
  书法: {
    title: '书法艺术',
    description: '中国传统汉字书写艺术，讲究笔法、结构和章法。',
    examples: ['篆书', '隶书', '楷书', '行书', '草书'],
    resources: ['书法入门', '历代书法名家'],
  },
  // ... 可以为其他知识点添加详情
};

const disciplinePairs = ref<DisciplinePair[]>([
  '美术+语文',
  '美术+数学',
  '美术+历史',
  '美术+地理',
  '美术+生物',
]);
const selectedDisciplinePair = ref<DisciplinePair>('美术+语文');
const showDetail = ref(false);
const currentDetail = ref<HotspotDetail | null>(null);

// 计算当前选中学科对应的图片路径
const currentImageSrc = computed(() => {
  return imageMap[selectedDisciplinePair.value];
});

// 获取当前选中的热区数据
const currentHotspots = computed(() => {
  return imageHotspots[selectedDisciplinePair.value] || [];
});

// 处理学科切换
const handleDisciplineChange = (value: DisciplinePair): void => {
  selectedDisciplinePair.value = value;
  console.log(`切换到学科: ${value}`);
};

// 处理热区点击
const handleHotspotClick = (hotspot: Hotspot): void => {
  const detail = hotspotDetails[hotspot.infoKey];
  if (detail) {
    currentDetail.value = detail;
    showDetail.value = true;
    console.log('Clicked hotspot:', hotspot.infoKey);
  } else {
    console.warn('No detail found for hotspot key:', hotspot.infoKey);
  }
};
</script>

<template>
  <el-card class="knowledge-graph-card">
    <template #header>
      <div class="card-header">
        <h3>
          <el-icon><Share /></el-icon> 学科星云
        </h3>
        <el-select
          v-model="selectedDisciplinePair"
          @change="handleDisciplineChange"
          class="discipline-select"
          placeholder="选择学科组合"
        >
          <el-option v-for="item in disciplinePairs" :key="item" :label="item" :value="item" />
        </el-select>
      </div>
    </template>
    <div class="image-container">
      <img
        :src="currentImageSrc"
        :alt="selectedDisciplinePair + ' 知识图谱'"
        class="knowledge-image"
      />
      <!-- 热区容器 -->
      <div class="hotspot-layer">
        <div
          v-for="hotspot in currentHotspots"
          :key="hotspot.id"
          class="hotspot"
          :style="hotspot.style"
          @click="handleHotspotClick(hotspot)"
          :title="hotspot.infoKey"
        ></div>
      </div>
    </div>
  </el-card>

  <!-- 详细信息对话框 -->
  <el-dialog
    v-model="showDetail"
    :title="currentDetail?.title"
    width="50%"
    :close-on-click-modal="false"
  >
    <div v-if="currentDetail" class="detail-content">
      <p class="description">{{ currentDetail.description }}</p>
      <div v-if="currentDetail.examples && currentDetail.examples.length > 0" class="examples">
        <h4>示例：</h4>
        <ul>
          <li v-for="(example, index) in currentDetail.examples" :key="index">
            {{ example }}
          </li>
        </ul>
      </div>
      <div v-if="currentDetail.resources && currentDetail.resources.length > 0" class="resources">
        <h4>相关资源：</h4>
        <ul>
          <li v-for="(resource, index) in currentDetail.resources" :key="index">
            {{ resource }}
          </li>
        </ul>
      </div>
    </div>
    <template #footer>
      <el-button @click="showDetail = false">关闭</el-button>
    </template>
  </el-dialog>
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
  padding: 15px 20px;
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

.discipline-select {
  width: 200px;
}

.image-container {
  width: 100%;
  height: 600px;
  display: flex; /* 使用flex布局 */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  padding: 10px;
  position: relative;
  overflow: visible;
}

.knowledge-image {
  max-width: 100%;
  max-height: 100%;
  height: auto;
  width: auto;
  display: block;
  border-radius: 4px;
  object-fit: contain;
  /* 移除margin，由flex布局自动居中 */
}

.hotspot-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none; /* 允许点击穿透到下面的热区 */
}

.hotspot {
  position: absolute;
  border: 2px dashed rgba(255, 0, 0, 0.3); /* 改为可见的红色虚线边框 */
  background-color: rgba(0, 255, 0, 0.1); /* 改为稍微可见的绿色背景 */
  cursor: pointer;
  transition:
    background-color 0.3s,
    border-color 0.3s;
  pointer-events: auto;
}

.hotspot:hover {
  background-color: rgba(0, 123, 255, 0.3); /* 悬停时高亮 */
  border-color: rgba(0, 123, 255, 0.7);
}

/* Detail Dialog Styles */
.detail-content {
  padding: 0 20px 20px; /* 调整内边距 */
}

.description {
  font-size: 16px;
  line-height: 1.6;
  margin-bottom: 20px;
  color: #333;
}

.examples,
.resources {
  margin-top: 20px;
}

h4 {
  color: #7353e5;
  margin-bottom: 10px;
  font-weight: bold;
}

ul {
  list-style-type: none;
  padding-left: 0;
}

li {
  margin-bottom: 8px;
  padding-left: 20px;
  position: relative;
  color: #555;
}

li::before {
  content: '•';
  color: #7353e5;
  position: absolute;
  left: 0;
  font-size: 1.2em; /* 稍微增大项目符号 */
  line-height: 1; /* 对齐 */
}
</style>
