import { request } from './index';

export interface PlanForm {
  subject: string;
  grade: string;
  topic: string;
  duration: number;
  objectives: string;
  keyPoints: string;
  teachingStyle: string;
  outputFormat: string;
}

export interface LessonPlanResponse {
  success: boolean;
  data: {
    title: string;
    content: string;
  };
}

// 生成教案
export async function generateLessonPlan(planForm: PlanForm): Promise<LessonPlanResponse> {
  // 真实环境下应该是:
  // return request.post('/teaching/plan', planForm);

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 2500));

  return {
    success: true,
    data: {
      title: `《${planForm.topic}》教学设计 (${planForm.subject} - ${planForm.grade})`,
      content:
        `# 《${planForm.topic}》教学设计\n\n` +
        `**教学学科**：${planForm.subject}\n` +
        `**适用年级**：${planForm.grade}\n` +
        `**教学课时**：${planForm.duration}分钟\n\n` +
        `**一、 教学目标**\n${planForm.objectives || '- 知识与技能：[根据课题自动填充或留空]\n- 过程与方法：[根据课题自动填充或留空]\n- 情感态度与价值观：[根据课题自动填充或留空]'}\n\n` +
        `**二、 教学重难点**\n- 重点：${planForm.keyPoints || '[根据课题自动填充或留空]'}\n- 难点：[根据课题自动填充或留空]\n\n` +
        `**三、 教学准备**\n- 教师：课件、相关视频/图片资料\n- 学生：预习相关内容\n\n` +
        `**四、 教学过程**\n\n` +
        `  1. 导入新课 (约5分钟)\n     - [激发学生兴趣，引入新课题]\n\n` +
        `  2. 讲解新知 (约20分钟)\n     - [详细讲解课题主要内容]\n     - [安排适当课堂活动]\n\n` +
        `  3. 巩固练习 (约15分钟)\n     - [设计针对性练习，学生独立或分组完成]\n     - [教师巡视指导，及时解答问题]\n\n` +
        `  4. 课堂小结与作业布置 (约5分钟)\n     - [师生共同总结，布置课后作业]\n\n` +
        `**五、 板书设计**\n[根据内容生成简洁板书框架]\n\n` +
        `**六、 教学反思**\n[留空供教师填写]\n`,
    },
  };
}
