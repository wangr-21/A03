<script setup lang="ts">
import { Link, InfoFilled } from '@element-plus/icons-vue';
import type { CaseItem } from '@/api';
import MarkdownIt from 'markdown-it';
import { computed } from 'vue';

const props = defineProps<{
  case_: CaseItem | null;
}>();

const visible = defineModel<boolean>('visible', { required: true });

const emit = defineEmits<{
  'view-story': [storyId: string];
}>();

const md = new MarkdownIt();

const renderedSuggestions = computed(() => {
  if (!props.case_?.implementation_suggestions) return '';
  return md.render(props.case_.implementation_suggestions);
});

function getResourceTagType(type: string): '' | 'success' | 'warning' | 'info' {
  const typeMap: Record<string, '' | 'success' | 'warning' | 'info'> = {
    document: '', // 文档使用默认颜色
    video: 'success', // 视频使用绿色
    audio: 'warning', // 音频使用黄色
    link: 'info', // 链接使用蓝色
  };
  return typeMap[type] || '';
}

function formatDate(dateStr: string): string {
  const date = new Date(dateStr);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}
</script>

<template>
  <el-dialog
    v-model="visible"
    :title="case_?.title"
    width="70%"
    destroy-on-close
    @update:visible="visible = $event"
  >
    <div v-if="case_" class="case-detail">
      <div class="meta-info">
        <el-tag class="meta-tag" size="small"> 主要学科: {{ case_.main_discipline }} </el-tag>
        <el-tag class="meta-tag" size="small" type="warning">
          相关学科: {{ case_.related_disciplines }}
        </el-tag>
        <el-tag class="meta-tag" size="small" type="info">
          适用年级: {{ case_.suitable_grades }}
        </el-tag>
      </div>

      <div class="content-section">
        <h4>教学目标</h4>
        <div class="scrollable-content">
          <p>{{ case_.teaching_objectives }}</p>
        </div>
      </div>

      <div class="content-section">
        <h4>案例内容</h4>
        <div class="scrollable-content">
          <p>{{ case_.content }}</p>
        </div>
      </div>

      <div v-if="case_.implementation_suggestions" class="content-section">
        <h4>实施建议</h4>
        <div class="scrollable-content" v-html="renderedSuggestions"></div>
      </div>

      <div v-if="case_.resources?.length" class="content-section">
        <h4>教学资源</h4>
        <div class="resources">
          <el-tag
            v-for="resource in case_.resources"
            :key="resource.title"
            :type="getResourceTagType(resource.type)"
            size="small"
            class="resource-tag"
          >
            <template v-if="resource.url">
              <a :href="resource.url" target="_blank" class="resource-link">
                {{ resource.title }}
                <el-icon class="link-icon"><Link /></el-icon>
              </a>
            </template>
            <template v-else>
              {{ resource.title }}
            </template>
            <el-tooltip v-if="resource.description" :content="resource.description" placement="top">
              <el-icon class="info-icon"><InfoFilled /></el-icon>
            </el-tooltip>
          </el-tag>
        </div>
      </div>

      <div class="footer">
        <div class="footer-actions">
          <el-button
            v-if="case_.story_id"
            type="primary"
            link
            @click="emit('view-story', case_.story_id)"
          >
            查看关联故事
          </el-button>
        </div>
        <span class="created-time">创建于 {{ formatDate(case_.created_at) }}</span>
      </div>
    </div>
  </el-dialog>
</template>

<style scoped>
.case-detail {
  .meta-info {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 20px;
  }

  .content-section {
    margin-bottom: 20px;

    h4 {
      font-size: 1em;
      margin-bottom: 10px;
      color: #303133;
    }

    .scrollable-content {
      max-height: 300px;
      overflow-y: auto;
      padding-right: 10px;
    }
  }

  .resources {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;

    .resource-tag {
      display: inline-flex;
      align-items: center;
      gap: 4px;

      .resource-link {
        color: inherit;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 4px;

        &:hover {
          text-decoration: underline;
        }

        .link-icon {
          font-size: 12px;
        }
      }

      .info-icon {
        margin-left: 4px;
        font-size: 12px;
        color: #909399;
      }
    }
  }

  .footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #ebeef5;
    padding-top: 15px;
    margin-top: 20px;

    .footer-actions {
      display: flex;
      gap: 10px;
    }

    .created-time {
      color: #909399;
      font-size: 0.9em;
    }
  }
}
</style>
