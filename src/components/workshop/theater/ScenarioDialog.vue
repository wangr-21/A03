<script setup lang="ts">
import type { Scenario } from '@/api/thinking';

defineProps<{
  scenario: Scenario | null;
}>();

const visible = defineModel('visible', {
  type: Boolean,
  default: false,
});

const scenarioTypeMap = {
  historical: { label: '历史情境', tag: 'warning' },
  literary: { label: '文学情境', tag: 'success' },
  scientific: { label: '科学情境', tag: 'info' },
} as const;

const getScenarioTypeLabel = (type: string): string => {
  return scenarioTypeMap[type as keyof typeof scenarioTypeMap]?.label || type;
};

const getScenarioTypeTag = (type: string): string => {
  return scenarioTypeMap[type as keyof typeof scenarioTypeMap]?.tag || 'info';
};
</script>

<template>
  <el-dialog
    v-model="visible"
    :title="scenario?.title"
    width="70%"
    @update:visible="visible = $event"
  >
    <div v-if="scenario">
      <div class="dialog-content">
        <div class="detail-header">
          <el-tag :type="getScenarioTypeTag(scenario.scenario_type)">
            {{ getScenarioTypeLabel(scenario.scenario_type) }}
          </el-tag>
          <div class="meta-tags">
            <el-tag size="small" effect="plain">{{ scenario.subject }}</el-tag>
            <el-tag size="small" effect="plain">{{ scenario.grade }}</el-tag>
          </div>
        </div>

        <div class="detail-section">
          <h4>场景背景</h4>
          <p>{{ scenario.background }}</p>
        </div>

        <div class="detail-section">
          <h4>教育价值</h4>
          <p>{{ scenario.educational_value }}</p>
        </div>

        <div class="detail-section">
          <h4>场景设计</h4>
          <el-collapse>
            <el-collapse-item
              v-for="scene in scenario.scenes"
              :key="scene.name"
              :title="scene.name"
            >
              <p>{{ scene.description }}</p>
              <div class="scene-elements">
                <div v-if="scene.visual_elements.length">
                  <h5>视觉元素</h5>
                  <ul>
                    <li v-for="(item, index) in scene.visual_elements" :key="index">
                      {{ item }}
                    </li>
                  </ul>
                </div>
                <div v-if="scene.audio_elements.length">
                  <h5>音频元素</h5>
                  <ul>
                    <li v-for="(item, index) in scene.audio_elements" :key="index">
                      {{ item }}
                    </li>
                  </ul>
                </div>
              </div>
            </el-collapse-item>
          </el-collapse>
        </div>

        <div class="detail-section">
          <h4>角色设定</h4>
          <el-descriptions
            v-for="char in scenario.characters"
            :key="char.name"
            :title="char.name"
            :column="1"
            border
          >
            <el-descriptions-item label="身份">
              {{ char.role }}
            </el-descriptions-item>
            <el-descriptions-item label="描述">
              {{ char.description }}
            </el-descriptions-item>
          </el-descriptions>
        </div>

        <div class="detail-section">
          <h4>教学指南</h4>
          <el-collapse accordion>
            <el-collapse-item title="场景设置">
              <ul>
                <li v-for="(item, index) in scenario.teacher_guide.setup" :key="index">
                  {{ item }}
                </li>
              </ul>
            </el-collapse-item>
            <el-collapse-item title="引导技巧">
              <ul>
                <li v-for="(item, index) in scenario.teacher_guide.facilitation_tips" :key="index">
                  {{ item }}
                </li>
              </ul>
            </el-collapse-item>
            <el-collapse-item title="反思问题">
              <ul>
                <li
                  v-for="(item, index) in scenario.teacher_guide.reflection_questions"
                  :key="index"
                >
                  {{ item }}
                </li>
              </ul>
            </el-collapse-item>
          </el-collapse>
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<style scoped>
.dialog-content {
  padding: 24px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

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

.detail-section h4 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #333;
  padding-bottom: 8px;
  border-bottom: 1px solid #eee;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 16px;
  background-color: #fff;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.meta-tags {
  display: flex;
  gap: 8px;
}

.scene-elements {
  margin-top: 16px;
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.scene-elements h5 {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #333;
}

.scene-elements ul {
  padding-left: 20px;
  margin: 0;
}

.scene-elements li {
  margin-bottom: 8px;
  line-height: 1.5;
}

/* Element Plus 组件样式覆盖 */
:deep(.el-collapse-item__content) {
  padding: 16px;
  background-color: #fff;
  border-radius: 4px;
}

:deep(.el-descriptions) {
  margin-bottom: 16px;
  padding: 16px;
  background-color: #fff;
  border-radius: 4px;
}

:deep(.el-descriptions:last-child) {
  margin-bottom: 0;
}

:deep(.el-collapse-item__header) {
  font-weight: 500;
  color: #333;
}

:deep(.el-descriptions__title) {
  font-size: 15px;
  font-weight: 600;
  color: #333;
}
</style>
