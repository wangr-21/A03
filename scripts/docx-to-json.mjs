import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import mammoth from 'mammoth';

/**
 * 此脚本用于将docx文件中的题目转换为JSON格式
 * 使用mammoth库解析docx文件中的题目内容
 */

// 获取当前文件的目录
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 定义输入和输出路径
const inputPath = path.resolve(__dirname, '../src/assets/demo/Question bank/bank_docx/question.docx');
const outputPath = path.resolve(__dirname, '../src/assets/demo/Question bank/bank_json/question.json');

// 确保输出目录存在
const outputDir = path.dirname(outputPath);
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

/**
 * 转换DOCX文件中的题目为JSON并保存
 */
async function convertDocxToJson() {
  try {
    // 检查输入文件是否存在
    if (!fs.existsSync(inputPath)) {
      throw new Error(`输入文件不存在: ${inputPath}`);
    }

    console.log(`正在读取文件: ${inputPath}`);

    // 使用mammoth提取docx文件中的文本内容
    const result = await mammoth.extractRawText({ path: inputPath });
    const text = result.value;

    // 将内容保存到临时文件供调试
    const debugPath = path.resolve(__dirname, '../temp-content.txt');
    fs.writeFileSync(debugPath, text);
    console.log(`提取的原始文本内容已保存到: ${debugPath}`);

    // 解析文本内容为题目对象
    console.log('正在解析题目内容...');
    const questions = parseQuestions(text);

    if (questions.length === 0) {
      throw new Error('未能解析出任何题目，请检查docx文件格式');
    }

    console.log(`成功解析出 ${questions.length} 道题目`);

    // 将结果写入JSON文件
    console.log(`正在写入JSON文件: ${outputPath}`);
    fs.writeFileSync(outputPath, JSON.stringify(questions, null, 2));

    console.log(`成功将题目数据写入JSON，已保存到: ${outputPath}`);
    console.log(`共保存了 ${questions.length} 道题目`);
  } catch (error) {
    console.error('转换过程中出错:', error.message);
    process.exit(1);
  }
}

/**
 * 从提取的文本内容中解析题目
 * @param {string} text 从docx提取的文本内容
 * @returns {Array} 题目数组
 */
function parseQuestions(text) {
  const questions = [];

  // 使用正则表达式分割文本，匹配"题号：数字"或"题目：数字"的模式
  const questionBlocks = text.split(/题号[：:]\s*\d+|\n\s*题号\s*\d+/);

  // 跳过第一个元素（如果是空的）
  let startIndex = 0;
  if (questionBlocks[0].trim() === '') {
    startIndex = 1;
  }

  console.log(`识别到 ${questionBlocks.length - startIndex} 个可能的题目块`);

  // 遍历每个题目块
  for (let i = startIndex; i < questionBlocks.length; i++) {
    const block = questionBlocks[i].trim();
    if (!block) continue;

    // 创建题目对象
    const question = {
      id: i,
      type: '',
      difficulty: '',
      point: '',
      subject: '',
      grade: '',
      stem: '',
      answer: '',
      explanation: ''
    };

    // 提取题目类型
    const typeMatch = block.match(/题目类型[：:]\s*(.+?)(?=\n|$)/);
    if (typeMatch) {
      question.type = typeMatch[1].trim();
    }

    // 提取难度
    const difficultyMatch = block.match(/难度[：:]\s*(.+?)(?=\n|$)/);
    if (difficultyMatch) {
      question.difficulty = difficultyMatch[1].trim();
    }

    // 提取知识点
    const pointMatch = block.match(/知识点[：:]\s*(.+?)(?=\n|$)/);
    if (pointMatch) {
      question.point = pointMatch[1].trim();
    }

    // 提取学科
    const subjectMatch = block.match(/学科[：:]\s*(.+?)(?=\n|$)/);
    if (subjectMatch) {
      question.subject = subjectMatch[1].trim();
    }

    // 提取年级
    const gradeMatch = block.match(/年级[：:]\s*(.+?)(?=\n|$)/);
    if (gradeMatch) {
      question.grade = gradeMatch[1].trim();
    }

    // 提取题干
    const stemMatch = block.match(/题干[：:]\s*(.+?)(?=\n选项[：:]|\n答案[：:]|\n解析[：:]|$)/s);
    if (stemMatch) {
      question.stem = stemMatch[1].trim();
    }

    // 提取选项（如果有）
    const optionsMatch = block.match(/选项[：:](?:\s*|\n)([\s\S]+?)(?=\n答案[：:]|\n解析[：:]|$)/);
    if (optionsMatch) {
      const optionsText = optionsMatch[1].trim();
      const options = [];

      // 使用正则表达式匹配选项
      const optionRegex = /([A-D])[.．、)\s]+([^\n]+)/g;
      let match;

      while ((match = optionRegex.exec(optionsText)) !== null) {
        options.push(match[2].trim());
      }

      if (options.length > 0) {
        question.options = options;
      }
    }

    // 提取答案
    const answerMatch = block.match(/答案[：:]\s*(.+?)(?=\n解析[：:]|$)/s);
    if (answerMatch) {
      question.answer = answerMatch[1].trim();
    }

    // 提取解析
    const explanationMatch = block.match(/解析[：:]\s*([\s\S]+?)$/);
    if (explanationMatch) {
      question.explanation = explanationMatch[1].trim();
    }

    // 只有当题目包含必要信息时才添加到列表中
    if (question.type && question.stem && question.answer) {
      questions.push(question);
    } else {
      console.warn(`警告: 跳过不完整的题目块 #${i}`);
    }
  }

  return questions;
}

// 执行转换
convertDocxToJson().catch(error => {
  console.error('程序执行错误:', error);
  process.exit(1);
});
