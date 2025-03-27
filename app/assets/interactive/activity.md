# 互动教学活动生成任务

## 基本信息

- 活动类型：{{activity_type}}
- 学科：{{subject}}
- 年级：{{grade}}
- 主题：{{topic}}
- 时长：{{duration}}分钟

## 请生成一个符合以下 JSON 格式的互动教学活动：

```json
{
  "title": "活动标题",
  "description": "活动简介和教学价值",
  "preparation": ["需要的准备材料1", "准备材料2"],
  "objectives": ["教学目标1", "教学目标2"],
  "steps": [
    {
      "name": "步骤1名称",
      "duration": X,
      "teacher_action": "教师活动描述",
      "student_action": "学生活动描述"
    },
    {
      "name": "步骤2名称",
      "duration": X,
      "teacher_action": "教师活动描述",
      "student_action": "学生活动描述"
    }
  ],
  "evaluation": {
    "criteria": ["评价标准1", "评价标准2"],
    "method": "评价方法描述"
  },
  "extensions": ["拓展活动1", "拓展活动2"]
}
```

## 设计要求

- 活动应具有互动性和趣味性
- 符合指定年级学生的认知水平
- 要有明确的教学价值
- 时间安排合理，符合指定总时长
- 对于"discussion"类型，提供有深度的讨论问题和引导策略
- 对于"question"类型，设计符合布鲁姆分类法的多层次问题
- 对于"game"类型，确保游戏规则清晰，并与学习内容相关
