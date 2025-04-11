<script setup lang="ts">
import { computed, ref } from 'vue';

const currentPage = ref(1);
const pageSize = ref(5);

const knowledgeData = [
  {
    key: '美术+语文',
    title: '山水意境创作课',
    description:
      '湖北监利市玉沙中学结合语文课文《山水画的意境》开展美术创作，学生通过赏析《漓江胜境图》并绘制心中山水，实现文本到图像的转化。',
    image: '/src/assets/datawithmix/images/literature.png',
    graph: '/src/assets/datawithmix/graphs/literature.png',
  },
  {
    key: '美术+历史',
    title: '文艺复兴艺术探源',
    description: '通过分析达芬奇《蒙娜丽莎》的构图与技法，理解人文主义精神。',
    image: '/src/assets/datawithmix/images/history.png',
    graph: '/src/assets/datawithmix/graphs/history.png',
  },
  {
    key: '美术+数学',
    title: '七巧板几何设计',
    description: '学生用七巧板拼几何图形并讲故事，融合数学规律与美术表达。',
    image: '/src/assets/datawithmix/images/math.png',
    graph: '/src/assets/datawithmix/graphs/math.png',
  },
  {
    key: '美术+生物',
    title: '生态主题绘画',
    description: '观察草履虫、仙人掌等生物结构后创作生态主题画作。',
    image: '/src/assets/datawithmix/images/biology.png',
    graph: '/src/assets/datawithmix/graphs/biology.png',
  },
  {
    key: '美术+地理',
    title: '地理摄影与地图绘制',
    description: '拍摄自然景观并绘制等高线地形图，结合地理知识解读作品。',
    image: '/src/assets/datawithmix/images/geography.png',
    graph: '/src/assets/datawithmix/graphs/geography.png',
  },
];

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return knowledgeData.slice(start, end);
});

const total = computed(() => knowledgeData.length);

const handleCurrentChange = (val: number) => {
  currentPage.value = val;
};
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
    <div class="card-list">
      <el-card v-for="item in paginatedData" :key="item.key">
        <div class="card-content">
          <div class="title-row">
            <h4 class="title">{{ item.title }}</h4>
            <el-tag size="small" type="primary">{{ item.key }}</el-tag>
          </div>
          <p class="description">{{ item.description }}</p>
          <img :src="item.graph" alt="知识图谱" class="graph-image" />
          <img :src="item.image" alt="课程图片" class="content-image" />
        </div>
      </el-card>
    </div>
    <div class="pagination-container">
      <el-pagination
        background
        layout="prev, pager, next"
        :total="total"
        :page-size="pageSize"
        :current-page="currentPage"
        @current-change="handleCurrentChange"
      />
    </div>
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

.card-list {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
  margin-top: 15px;
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.card-content .title {
  font-size: 16px;
  font-weight: bold;
  margin: 0;
  color: #333;
}

.card-content .description {
  color: #666;
  font-size: 14px;
  line-height: 1.5;
  margin: 0;
}

.card-content .graph-image,
.card-content .content-image {
  width: 100%;
  border-radius: 4px;
  object-fit: cover;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

@media screen and (max-width: 1200px) {
  .card-list {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media screen and (max-width: 768px) {
  .card-list {
    grid-template-columns: 1fr;
  }
}

.title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 0;
}

.title-row .title {
  font-size: 16px;
  font-weight: bold;
  margin: 0;
  color: #333;
}
</style>
