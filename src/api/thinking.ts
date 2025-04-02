import { request } from './index';

// 互动环节数据结构
export interface Interaction {
  id: number;
  type: string;
  title: string;
  content: string;
  tags: string[];
}

// 情景模拟数据结构
export interface Scenario {
  id: number;
  title: string;
  description: string;
  background: string;
  objectives: string[];
  difficulty: string;
}

export interface InteractionFilters {
  type?: string;
  tag?: string;
}

export interface InteractionNote {
  interactionId: number;
  topic: string;
  duration: number;
  notes: string;
}

export interface ScenarioResult {
  scenarioId: number;
  response: string;
}

// 获取互动环节列表
export async function getInteractions(filters: InteractionFilters = {}): Promise<Interaction[]> {
  // 真实环境下应该是:
  // return request.get('/thinking/interactions', { params: filters });

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 800));

  const interactions: Interaction[] = [
    {
      id: 1,
      type: '提问策略',
      title: '苏格拉底式提问法',
      content:
        '通过一系列引导性问题，帮助学生自己发现知识点和解决问题的方法。\n1. 你认为...的核心概念是什么？请用自己的话解释。\n2. 这个概念与我们之前学过的...有什么联系？\n3. 如果改变...中的某个条件，可能会产生什么不同的结果？',
      tags: ['批判性思维', '高阶思维', '通用'],
    },
    {
      id: 2,
      type: '小组活动',
      title: '思维导图协作',
      content:
        '将学生分成4-5人小组，每组使用一张大纸，围绕中心概念创建思维导图，展示概念间的联系。\n- 第一阶段(10分钟)：每人负责一个分支\n- 第二阶段(5分钟)：小组讨论并连接不同分支\n- 第三阶段(5分钟)：小组展示',
      tags: ['合作学习', '可视化', '知识整合'],
    },
    {
      id: 3,
      type: '思辨讨论',
      title: '六顶思考帽',
      content:
        '使用六顶思考帽方法进行多角度思考：\n- 白帽：关注客观事实和数据\n- 红帽：表达情感和直觉反应\n- 黑帽：指出风险和问题\n- 黄帽：寻找优点和价值\n- 绿帽：提出创新和替代方案\n- 蓝帽：负责总结和流程控制',
      tags: ['多角度思考', '结构化讨论', '高中适用'],
    },
    {
      id: 4,
      type: '角色扮演',
      title: '历史人物对话',
      content:
        '学生扮演不同历史时期或不同立场的人物，围绕特定话题进行对话或辩论。\n准备阶段：\n- 研究人物背景和观点\n- 准备符合人物身份的论点\n表演阶段：\n- 按照时间线或议题展开对话\n- 其他学生可提问或评论',
      tags: ['历史', '语文', '跨学科'],
    },
  ];

  // 应用筛选
  return interactions.filter((item) => {
    if (filters.type && item.type !== filters.type) return false;
    if (filters.tag && !item.tags.includes(filters.tag)) return false;
    return true;
  });
}

// 获取情景模拟列表
export async function getScenarios(): Promise<Scenario[]> {
  // 真实环境下应该是:
  // return request.get('/thinking/scenarios');

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 800));

  return [
    {
      id: 1,
      title: '古诗创作场景',
      description: '模拟古代文人雅集场景，引导学生体验古诗创作过程',
      background:
        '你身处盛唐长安，正值春日，与友人在城外踏青赏花。看着眼前的美景，你准备即兴创作一首七言绝句...',
      objectives: ['理解古诗创作背景', '掌握七言绝句格律', '培养文学鉴赏能力'],
      difficulty: '中等',
    },
    {
      id: 2,
      title: '科学探究实验室',
      description: '模拟科学家进行实验探究的过程，培养科学思维和方法',
      background:
        '你是一位年轻的科学家，正在研究植物生长与环境因素的关系。你需要设计一个实验，控制变量并收集数据...',
      objectives: ['学习科学实验设计', '理解变量控制原理', '培养数据分析能力'],
      difficulty: '较难',
    },
    {
      id: 3,
      title: '历史决策模拟',
      description: '置身历史关键时刻，模拟历史人物面临的决策困境',
      background:
        '公元1839年，你是清朝钦差大臣林则徐，奉命到广州查禁鸦片。面对外国商人的抵制和朝廷的压力，你需要决定如何处理查获的鸦片...',
      objectives: ['理解历史背景与影响因素', '培养多角度分析能力', '锻炼决策思维'],
      difficulty: '较难',
    },
    {
      id: 4,
      title: '数学应用情境',
      description: '将抽象数学概念应用到实际生活情境中',
      background:
        '你是一名建筑师，正在设计一座新的城市广场。你需要运用几何知识设计出美观且实用的空间布局...',
      objectives: ['理解数学在实际中的应用', '培养空间思维能力', '锻炼问题解决能力'],
      difficulty: '中等',
    },
  ];
}

// 创建新互动环节
export async function createInteraction(data: Omit<Interaction, 'id'>): Promise<Interaction> {
  // 真实环境下应该是:
  // return request.post('/thinking/interactions', data);

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 1000));

  return {
    id: Date.now(),
    ...data,
  };
}

// 创建新情景模拟
export async function createScenario(data: Omit<Scenario, 'id'>): Promise<Scenario> {
  // 真实环境下应该是:
  // return request.post('/thinking/scenarios', data);

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 1000));

  return {
    id: Date.now(),
    ...data,
  };
}

// 保存互动应用结果
export async function saveInteractionNote(note: InteractionNote): Promise<{ success: boolean }> {
  // 真实环境下应该是:
  // return request.post('/thinking/interaction-notes', note);

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 600));

  return {
    success: true,
  };
}

// 提交情景模拟结果
export async function submitScenarioResult(result: ScenarioResult): Promise<{ success: boolean }> {
  // 真实环境下应该是:
  // return request.post('/thinking/scenario-results', result);

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 600));

  return {
    success: true,
  };
}
