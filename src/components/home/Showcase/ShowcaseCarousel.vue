<script setup lang="ts">
import showcaseImages from '@/assets/demo/showcase';

interface CarouselItem {
  id: number;
  title: string;
  description: string;
  image: string;
}

// 轮播数据
const carouselItems: CarouselItem[] = [
  {
    id: 1,
    title: '优秀教学案例展示',
    description: '互动式课堂设计',
    image: showcaseImages.carousel1,
  },
  {
    id: 2,
    title: '学生创意作品欣赏',
    description: 'AI赋能美术创作',
    image: showcaseImages.carousel2,
  },
  {
    id: 3,
    title: '最新平台功能介绍',
    description: '学科星云知识图谱上线',
    image: showcaseImages.carousel3,
  },
];
</script>

<template>
  <el-card class="carousel-card">
    <el-carousel height="300px" arrow="always">
      <el-carousel-item v-for="item in carouselItems" :key="item.id">
        <img :src="item.image" class="carousel-image" />
        <div class="carousel-caption">
          <h3>{{ item.title }}</h3>
          <p>{{ item.description }}</p>
        </div>
      </el-carousel-item>
    </el-carousel>
  </el-card>
</template>

<style scoped>
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
</style>
