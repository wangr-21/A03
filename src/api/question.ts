import { request } from './index';

export interface QuestionFilters {
  type: string[];
  difficulty: string;
  knowledgePoint: string;
  page?: number;
  pageSize?: number;
  subject?: string;
  searchTerm?: string;
}

export interface Question {
  id: number;
  type: string;
  difficulty: string;
  point: string;
  stem: string;
  answer: string;
  options?: string[];
  explanation?: string;
  subject?: string;
  grade?: string;
}

export interface QuestionsResponse {
  success: boolean;
  data: {
    questions: Question[];
    total: number;
  };
}

// 题目类型常量
export const QUESTION_TYPES = ['选择题', '填空题', '解答题', '判断题', '连线题', '综合题'];
export const DIFFICULTY_LEVELS = ['easy', 'medium', 'hard'];
export const KNOWLEDGE_POINTS = [
  '函数',
  '几何',
  '代数',
  '概率统计',
  '物理力学',
  '化学反应',
  '文言文',
  '现代文阅读',
  '英语语法',
];
export const SUBJECTS = ['数学', '语文', '英语', '物理', '化学', '历史', '地理', '生物', '政治'];

// 模拟题库数据
const allQuestions: Question[] = [
  {
    id: 1,
    type: '选择题',
    difficulty: 'easy',
    point: '函数',
    subject: '数学',
    grade: '初中',
    stem: '下列哪个是函数 y = 2x + 1 的图像？',
    options: ['一条向右上方倾斜的直线', '一条向右下方倾斜的直线', '一条水平直线', '一条垂直直线'],
    answer: 'A',
    explanation: '函数y=2x+1是一次函数，斜率为2大于0，所以是向右上方倾斜的直线。',
  },
  {
    id: 2,
    type: '填空题',
    difficulty: 'medium',
    point: '几何',
    subject: '数学',
    grade: '初中',
    stem: '三角形内角和是____度。',
    answer: '180',
    explanation: '平面内任意三角形的内角和都等于180°。',
  },
  {
    id: 3,
    type: '选择题',
    difficulty: 'medium',
    point: '概率统计',
    subject: '数学',
    grade: '高中',
    stem: '袋中有3个红球和2个白球，随机摸出2个球，摸出的球都是红球的概率是多少？',
    options: ['1/10', '3/10', '3/5', '1/5'],
    answer: 'C',
    explanation: '总共有C(5,2)=10种摸法，摸出2个红球的方法有C(3,2)=3种，所以概率为3/10。',
  },
  {
    id: 4,
    type: '判断题',
    difficulty: 'easy',
    point: '物理力学',
    subject: '物理',
    grade: '高中',
    stem: '物体做自由落体运动时，其加速度大小与物体的质量有关。',
    answer: '错误',
    explanation: '自由落体运动的加速度大小等于重力加速度g，与物体质量无关。',
  },
  {
    id: 5,
    type: '解答题',
    difficulty: 'hard',
    point: '代数',
    subject: '数学',
    grade: '高中',
    stem: '解方程：x² - 5x + 6 = 0',
    answer: 'x = 2 或 x = 3',
    explanation: '使用因式分解法：x² - 5x + 6 = (x-2)(x-3) = 0，解得x = 2 或 x = 3。',
  },
  {
    id: 6,
    type: '选择题',
    difficulty: 'medium',
    point: '化学反应',
    subject: '化学',
    grade: '高中',
    stem: '下列关于氧化还原反应的说法中，错误的是：',
    options: [
      '氧化反应一定伴随着还原反应',
      '氧化是指失电子的过程',
      '所有燃烧反应都是氧化还原反应',
      '氧化剂的化合价在反应前后一定升高',
    ],
    answer: 'D',
    explanation: '氧化剂在反应中得到电子，所以它的化合价降低而不是升高。',
  },
  {
    id: 7,
    type: '填空题',
    difficulty: 'easy',
    point: '文言文',
    subject: '语文',
    grade: '初中',
    stem: '"不畏浮云遮望眼"的下一句是：________。',
    answer: '只缘身在最高层',
    explanation: '出自王安石的《登飞来峰》，完整的诗句是"不畏浮云遮望眼，只缘身在最高层"。',
  },
  {
    id: 8,
    type: '解答题',
    difficulty: 'hard',
    point: '现代文阅读',
    subject: '语文',
    grade: '高中',
    stem: '阅读下面的文字，回答问题：\n鲁迅先生曾说："愿中国青年都摆脱冷气，只是向上走，不必听自暴自弃者流的话。能做事的做事，能发声的发声。"这段话表达了作者怎样的思想感情？',
    answer:
      '这段话表达了鲁迅先生对中国青年的殷切期望，希望他们保持进取精神，不被消极情绪影响，积极行动起来，为改变社会现状贡献自己的力量。',
    explanation: '这是鲁迅在《热风·随感录四十一》中的名言，表达了他对青年人的期望和鼓励。',
  },
  {
    id: 9,
    type: '选择题',
    difficulty: 'medium',
    point: '英语语法',
    subject: '英语',
    grade: '高中',
    stem: 'I _____ TV when the phone rang.',
    options: ['watched', 'was watching', 'am watching', 'have watched'],
    answer: 'B',
    explanation: '当电话响起时，"我"正在看电视，表示过去某一时刻正在进行的动作，应使用过去进行时。',
  },
  {
    id: 10,
    type: '连线题',
    difficulty: 'medium',
    point: '几何',
    subject: '数学',
    grade: '初中',
    stem: '将下列图形与其对应的面积计算公式连接起来：\nA.正方形 B.圆形 C.三角形 D.梯形\n1.S=πr² 2.S=a² 3.S=(a+b)h/2 4.S=ah/2',
    answer: 'A-2,B-1,C-4,D-3',
    explanation:
      '正方形面积公式S=a²，圆形面积公式S=πr²，三角形面积公式S=ah/2，梯形面积公式S=(a+b)h/2。',
  },
  {
    id: 11,
    type: '判断题',
    difficulty: 'easy',
    point: '物理力学',
    subject: '物理',
    grade: '初中',
    stem: '牛顿第一定律又称为惯性定律。',
    answer: '正确',
    explanation:
      '牛顿第一定律描述了物体在没有外力作用下保持静止或匀速直线运动状态的趋势，这种趋势就是惯性，因此也称为惯性定律。',
  },
  {
    id: 12,
    type: '解答题',
    difficulty: 'hard',
    point: '代数',
    subject: '数学',
    grade: '高中',
    stem: '已知等比数列{an}的前n项和为Sn，若a1=1，S3=7，求该数列的通项公式。',
    answer: 'an = 3^(n-1)',
    explanation:
      '设公比为q，则S3 = (1-q^3)/(1-q) = 7。由于a1=1，所以S3 = 1+q+q^2 = 7，解得q=3，因此an = a1*q^(n-1) = 3^(n-1)。',
  },
  {
    id: 13,
    type: '选择题',
    difficulty: 'easy',
    point: '化学反应',
    subject: '化学',
    grade: '初中',
    stem: '下列物质属于纯净物的是：',
    options: ['空气', '牛奶', '自来水', '蒸馏水'],
    answer: 'D',
    explanation:
      '纯净物是由同种物质组成的物质。空气由氮气、氧气等组成，是混合物；牛奶含有水、蛋白质等，是混合物；自来水含有多种溶解物，是混合物；蒸馏水基本上只含有H2O，是纯净物。',
  },
  {
    id: 14,
    type: '填空题',
    difficulty: 'medium',
    point: '文言文',
    subject: '语文',
    grade: '高中',
    stem: '《曹刿论战》中，"小惠未徧，民弗从也"中"徧"的意思是________。',
    answer: '普遍',
    explanation:
      '"小惠未徧"意思是小恩小惠不普遍，表明了统治者如果只对少数人施以小恩小惠，而没有普遍惠及民众，民众就不会服从和拥护。',
  },
  {
    id: 15,
    type: '综合题',
    difficulty: 'hard',
    point: '概率统计',
    subject: '数学',
    grade: '高中',
    stem: '某班级共有40名学生，其中男生占60%。从该班级随机抽取4名学生进行问卷调查，求抽到的4名学生都是男生的概率。如果已知抽到的第一个学生是男生，求剩下抽到的3名学生都是男生的概率。',
    answer: '第一问：约为0.1296或12.96%\n第二问：约为0.216或21.6%',
    explanation:
      '第一问：共有40名学生，其中男生有40×60%=24名。抽取4名学生都是男生的概率为C(24,4)/C(40,4)=(24×23×22×21)/(40×39×38×37)≈0.1296。\n第二问：已知第一个是男生，则在剩下的39名学生中有23名男生，抽取3名都是男生的概率为C(23,3)/C(39,3)=(23×22×21)/(39×38×37)≈0.216。',
  },
];

// 获取题目列表
export async function getQuestions(filters: QuestionFilters): Promise<QuestionsResponse> {
  // 真实环境下应该是:
  // return request.get('/question-bank/questions', { params: filters });

  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 800));

  // 筛选题目
  let filteredQuestions = [...allQuestions];

  // 按题型筛选
  if (filters.type && filters.type.length > 0) {
    filteredQuestions = filteredQuestions.filter((q) => filters.type.includes(q.type));
  }

  // 按难度筛选
  if (filters.difficulty && filters.difficulty !== 'all') {
    filteredQuestions = filteredQuestions.filter((q) => q.difficulty === filters.difficulty);
  }

  // 按知识点筛选
  if (filters.knowledgePoint && filters.knowledgePoint !== 'all') {
    filteredQuestions = filteredQuestions.filter((q) => q.point === filters.knowledgePoint);
  }

  // 按学科筛选
  if (filters.subject && filters.subject !== 'all') {
    filteredQuestions = filteredQuestions.filter((q) => q.subject === filters.subject);
  }

  // 关键词搜索
  if (filters.searchTerm) {
    const keyword = filters.searchTerm.toLowerCase();
    filteredQuestions = filteredQuestions.filter(
      (q) =>
        q.stem.toLowerCase().includes(keyword) ||
        q.point.toLowerCase().includes(keyword) ||
        (q.explanation && q.explanation.toLowerCase().includes(keyword)),
    );
  }

  // 分页
  const page = filters.page || 1;
  const pageSize = filters.pageSize || 10;
  const startIndex = (page - 1) * pageSize;
  const endIndex = startIndex + pageSize;
  const paginatedQuestions = filteredQuestions.slice(startIndex, endIndex);

  return {
    success: true,
    data: {
      questions: paginatedQuestions,
      total: filteredQuestions.length,
    },
  };
}

// 获取题目详情
export async function getQuestionDetail(
  id: number,
): Promise<{ success: boolean; data: Question | null }> {
  // 模拟API调用
  await new Promise((resolve) => setTimeout(resolve, 500));

  const question = allQuestions.find((q) => q.id === id) || null;

  return {
    success: !!question,
    data: question,
  };
}
