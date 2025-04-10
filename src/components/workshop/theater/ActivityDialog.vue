<script setup lang="ts">
import type { Activity } from '@/api/thinking';

defineProps<{
  activity: Activity | null;
}>();

const visible = defineModel<boolean>('visible', { required: true });

// 活动类型标签和文本映射
const activityTypeMap = {
  discussion: { label: '讨论', tag: 'success' },
  question: { label: '提问', tag: 'primary' },
  game: { label: '游戏', tag: 'warning' },
} as const;

const getActivityTypeLabel = (type: string): string => {
  return activityTypeMap[type as keyof typeof activityTypeMap]?.label || type;
};

const getActivityTypeTag = (type: string): string => {
  return activityTypeMap[type as keyof typeof activityTypeMap]?.tag || 'info';
};
</script>

<template>
  <el-dialog
    v-model="visible"
    :title="activity?.title"
    width="60%"
    @update:visible="visible = $event"
  >
    <div v-if="activity">
      <div class="dialog-content">
        <div class="detail-header">
          <el-tag :type="getActivityTypeTag(activity.activity_type)">
            {{ getActivityTypeLabel(activity.activity_type) }}
          </el-tag>
          <div class="meta-tags">
            <el-tag size="small" effect="plain">{{ activity.subject }}</el-tag>
            <el-tag size="small" effect="plain">{{ activity.grade }}</el-tag>
            <el-tag size="small" effect="plain">{{ activity.duration }}分钟</el-tag>
          </div>
        </div>

        <!-- 活动描述 -->
        <div class="detail-section">
          <h4>活动描述</h4>
          <p>{{ activity.description }}</p>
        </div>

        <!-- 活动准备 -->
        <div class="detail-section">
          <h4>活动准备</h4>
          <ul>
            <li v-for="(item, index) in activity.preparation" :key="index">
              {{ item }}
            </li>
          </ul>
        </div>

        <!-- 活动目标 -->
        <div class="detail-section">
          <h4>活动目标</h4>
          <ul>
            <li v-for="(item, index) in activity.objectives" :key="index">
              {{ item }}
            </li>
          </ul>
        </div>

        <!-- 活动步骤 -->
        <div class="detail-section">
          <h4>活动步骤</h4>
          <el-timeline>
            <el-timeline-item
              v-for="step in activity.steps"
              :key="step.name"
              :timestamp="`${step.duration}分钟`"
            >
              <h5>{{ step.name }}</h5>
              <p>教师：{{ step.teacher_action }}</p>
              <p>学生：{{ step.student_action }}</p>
            </el-timeline-item>
          </el-timeline>
        </div>

        <!-- 评价方式 -->
        <div class="detail-section">
          <h4>评价方式</h4>
          <p>{{ activity.evaluation.method }}</p>
          <el-empty v-if="activity.evaluation.criteria.length === 0" description="暂无评价标准" />
          <ul v-else>
            <li v-for="(item, index) in activity.evaluation.criteria" :key="index">
              {{ item }}
            </li>
          </ul>
        </div>

        <!-- 延伸活动 -->
        <div class="detail-section">
          <h4>延伸活动</h4>
          <el-empty v-if="activity.extensions.length === 0" description="暂无延伸活动" />
          <ul v-else>
            <li v-for="(item, index) in activity.extensions" :key="index">
              {{ item }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<style scoped>
.detail-section {
  padding: 20px;
  background-color: #fff;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  margin-bottom: 24px;
}

/* 最后一个 section 不需要底部间距 */
.detail-section:last-child {
  margin-bottom: 0;
}

/* 优化标题样式 */
.detail-section h4 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #333;
  padding-bottom: 8px;
  border-bottom: 1px solid #eee;
}

/* 调整列表样式 */
.detail-section ul {
  padding-left: 20px;
  margin: 0;
}

.detail-section li {
  margin-bottom: 8px;
  line-height: 1.5;
}

.detail-section li:last-child {
  margin-bottom: 0;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.meta-tags {
  display: flex;
  gap: 8px;
}

.dialog-content {
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
}
</style>
