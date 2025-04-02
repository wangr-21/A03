import { request } from './index';

export interface InteractionItem {
  type: string;
  title: string;
  content: string;
}

export interface InteractionResponse {
  success: boolean;
  data: InteractionItem[];
}

// 获取推荐互动
export async function getRecommendedInteractions(topic: string): Promise<InteractionResponse> {
  // 真实环境下应该是:
  // return request.get('/interactive/recommendations', { params: { topic } });

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 1500));

  return {
    success: true,
    data: [
      {
        type: '提问策略',
        title: `针对"${topic}"的开放式提问`,
        content:
          `1. 思考启发：${topic}的核心要素有哪些？它们之间有什么联系？\n` +
          `2. 探究发散：如果改变其中的某个条件，会产生什么不同的结果？\n` +
          `3. 生活关联：你能举出生活中与${topic}相关的实例吗？\n` +
          `4. 跨学科思考：这个概念在其他学科中有什么应用？\n` +
          `5. 价值判断：学习${topic}对我们有什么意义和价值？`,
      },
      {
        type: '小组活动',
        title: `"${topic}"协作探究活动`,
        content:
          `活动流程：\n` +
          `1. 将学生分成4-5人小组\n` +
          `2. 每组分配不同的研究角度，准备5分钟\n` +
          `3. 小组内部讨论10分钟，整理观点\n` +
          `4. 各小组选代表进行3分钟汇报\n` +
          `5. 全班评议，教师总结\n\n` +
          `建议工具：思维导图、角色扮演、实物展示`,
      },
      {
        type: '辩论设计',
        title: `关于"${topic}"的辩论活动`,
        content:
          `辩题建议：${topic}的利与弊\n\n` +
          `活动设计：\n` +
          `1. 提前一周布置资料收集任务\n` +
          `2. 课堂上分正反方，每方4-5人\n` +
          `3. 每位学生有2分钟发言时间\n` +
          `4. 教师担任主持，其余学生担任评委\n\n` +
          `设置正反方观点，让学生自由选择立场，进行小型辩论，鼓励学生引用学习内容支持自己的观点，培养批判性思维。`,
      },
    ],
  };
}
