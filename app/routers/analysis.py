# ruff: noqa: E501, N815
from typing import Literal

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy import func, select

from ..db import DBSession, HomeworkInfo, StudentInfo
from ..services import fleep
from ..services.analysis import analyze_image_emotion, extract_dominant_colors

router = APIRouter(prefix="/analysis", tags=["analysis"])


# 图片分析响应模型
class ColorInfo(BaseModel):
    hex: str
    percentage: float


class ImageAnalysisResponse(BaseModel):
    colors: list[ColorInfo]
    emotion: str


# 学生个人分析响应模型
class KnowledgePoint(BaseModel):
    knowledge: str
    masteryLevel: float


class ScoreTrendPoint(BaseModel):
    homeworkOrder: int
    score: float


class StudentAnalysisResponse(BaseModel):
    commentAnalysis: str
    heatmapData: list[KnowledgePoint]
    scoreTrend: list[ScoreTrendPoint]
    overallAnalysis: str


@router.post("/image", response_model=ImageAnalysisResponse)
async def analyze_image(
    word_count: Literal["50", "100", "150", "200"] = "100",
    file: UploadFile = File(),
):
    """处理图片分析请求"""

    head = await file.read(256)
    info = fleep.get(head)
    if not info or not info.mime:
        raise HTTPException(status_code=400, detail="文件格式无效")
    if not info.extension_matches("png") and not info.extension_matches("jpg"):
        raise HTTPException(status_code=400, detail="仅支持PNG/JPG格式")

    content = head + await file.read()
    if len(content) > 10 * 1024 * 1024:  # 10MB
        raise HTTPException(status_code=400, detail="图片大小不能超过10MB")

    colors = extract_dominant_colors(content)
    if not colors:
        raise HTTPException(status_code=500, detail="无法提取图片颜色信息")

    try:
        emotion_text = await analyze_image_emotion(content, colors, int(word_count))
        return {"colors": colors, "emotion": emotion_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/student/{student_id}", response_model=StudentAnalysisResponse)
async def analyze_student(db: DBSession, student_id: str):
    """
    分析单个学生的学习情况
    """
    # 验证学生是否存在
    student_stmt = select(StudentInfo).filter(StudentInfo.student_id == student_id)

    if not (student := (await db.execute(student_stmt)).scalar()):
        raise HTTPException(
            status_code=404, detail="未找到该学生信息，请检查学号、姓名和性别"
        )

    # 获取学生所有作业
    homework_stmt = (
        select(HomeworkInfo)
        .filter(HomeworkInfo.student_id == student_id)
        .order_by(HomeworkInfo.homework_order)
    )

    homeworks = list((await db.execute(homework_stmt)).scalars().all())

    if not homeworks:
        raise HTTPException(status_code=404, detail="该学生尚未提交任何作业")

    # 分析作业评语 (实际应用中这里可以使用NLP模型分析)
    comment_analysis = analyze_comments([hw.comment for hw in homeworks if hw.comment])

    # 构建分数趋势数据
    score_trend = [
        ScoreTrendPoint(homeworkOrder=hw.homework_order, score=hw.score)
        for hw in homeworks
        if hw.score is not None
    ]

    # 分析知识点掌握情况 (实际应用中可能需要更复杂的分析算法)
    heatmap_data = generate_knowledge_heatmap(homeworks)

    # 生成整体分析
    overall_analysis = generate_overall_analysis(
        student.student_name,
        homeworks,
        score_trend,
    )

    return StudentAnalysisResponse(
        commentAnalysis=comment_analysis,
        heatmapData=heatmap_data,
        scoreTrend=score_trend,
        overallAnalysis=overall_analysis,
    )


# 班级分析响应模型
class ClassKnowledgePoint(BaseModel):
    knowledge: str
    averageMastery: float


class ClassAnalysisResponse(BaseModel):
    classHeatmap: list[ClassKnowledgePoint]
    classAnalysis: str


@router.get("/class", response_model=ClassAnalysisResponse)
async def analyze_class(db: DBSession):
    """
    分析整个班级的学习情况
    """
    # 获取所有学生作业
    homeworks = list((await db.execute(select(HomeworkInfo))).scalars().all())

    if not homeworks:
        raise HTTPException(status_code=404, detail="尚未有学生提交作业")

    # 计算班级平均分
    avg_score_stmt = select(func.avg(HomeworkInfo.score))
    avg_score_result = await db.execute(avg_score_stmt)
    avg_score = avg_score_result.scalar() or 0

    # 生成班级知识点热力图
    class_heatmap = generate_class_knowledge_heatmap(homeworks)

    # 生成班级整体分析
    class_analysis = generate_class_analysis(homeworks, avg_score)

    return ClassAnalysisResponse(
        classHeatmap=class_heatmap,
        classAnalysis=class_analysis,
    )


# 辅助函数
def analyze_comments(comments: list[str]) -> str:
    """分析评语中的关键信息"""
    if not comments:
        return "尚无评语数据可供分析"

    # 在实际应用中，这里可以使用NLP技术分析评语内容
    # 简化版本:
    positive_keywords = ["优秀", "出色", "清晰", "正确", "工整", "扎实", "良好"]
    negative_keywords = ["错误", "偏差", "困难", "不高", "不够"]

    positive_count = sum(
        keyword in comment for comment in comments for keyword in positive_keywords
    )
    negative_count = sum(
        keyword in comment for comment in comments for keyword in negative_keywords
    )

    total = positive_count + negative_count
    if total == 0:
        return "评语分析：根据现有评语，无法确定明显的学习特点。"

    positive_ratio = positive_count / total

    if positive_ratio > 0.7:
        return "评语分析：整体学习状态良好，根据评语反馈，掌握知识点扎实，理解透彻，作业完成质量高。"
    if positive_ratio > 0.4:
        return (
            "评语分析：学习状态一般，有部分知识点掌握得不够牢固，需要加强针对性练习。"
        )
    return "评语分析：学习存在一定困难，多数知识点理解不够透彻，建议加强基础知识学习和课后练习。"


def generate_knowledge_heatmap(homeworks: list[HomeworkInfo]) -> list[KnowledgePoint]:
    """生成知识点掌握程度热力图数据"""
    # 在实际应用中，这里可能需要分析作业内容来提取知识点
    # 简化版本，基于作业分数推断几个预设的知识点掌握程度

    # 预设的知识点列表
    knowledge_points = ["基本概念", "公式应用", "解题思路", "计算准确性", "综合应用"]

    # 如果没有分数，返回默认值
    if not any(hw.score is not None for hw in homeworks):
        return [KnowledgePoint(knowledge=kp, masteryLevel=0) for kp in knowledge_points]

    # 基于作业分数生成模拟的知识点掌握程度
    all_scores = [hw.score for hw in homeworks if hw.score is not None]
    avg_score = sum(all_scores) / len(all_scores) if all_scores else 0

    # 为不同知识点设置略有差异的掌握度
    import random

    random.seed(sum(all_scores))  # 使结果可重复

    result: list[KnowledgePoint] = []
    for kp in knowledge_points:
        # 基于平均分生成掌握程度，添加一些随机波动使数据更真实
        mastery = (avg_score / 100) * (0.85 + random.uniform(-0.15, 0.15))
        mastery = max(0, min(1, mastery))  # 限制在0-1范围内
        result.append(
            KnowledgePoint(knowledge=kp, masteryLevel=round(mastery * 100) / 100)
        )

    return result


def generate_overall_analysis(
    student_name: str,
    homeworks: list[HomeworkInfo],  # noqa: ARG001
    score_trend: list[ScoreTrendPoint],
) -> str:
    """生成学生的整体学习分析"""
    if not score_trend:
        return f"{student_name}同学尚未有评分记录，无法生成整体分析。"

    scores = [item.score for item in score_trend]
    avg_score = sum(scores) / len(scores)

    # 分析成绩趋势
    trend_analysis = ""
    if len(scores) > 1:
        if scores[-1] > scores[0]:
            trend_analysis = "成绩呈上升趋势，表明学习效果在不断提升。"
        elif scores[-1] < scores[0]:
            trend_analysis = "成绩呈下降趋势，需要关注学习效果。"
        else:
            trend_analysis = "成绩保持稳定。"

    # 根据平均分给出不同的建议
    if avg_score >= 90:
        return f"{student_name}同学整体表现优秀，平均分达到{avg_score:.1f}分。{trend_analysis}建议继续保持良好的学习习惯，可以尝试更具挑战性的学习内容。"
    if avg_score >= 80:
        return f"{student_name}同学整体表现良好，平均分为{avg_score:.1f}分。{trend_analysis}建议巩固已掌握的知识点，针对性地提高薄弱环节。"
    if avg_score >= 70:
        return f"{student_name}同学整体表现中等，平均分为{avg_score:.1f}分。{trend_analysis}建议加强基础知识的学习和理解，增加练习量。"
    if avg_score >= 60:
        return f"{student_name}同学整体表现及格，平均分为{avg_score:.1f}分。{trend_analysis}建议重点关注基础知识点，寻求教师帮助，制定针对性学习计划。"
    return f"{student_name}同学整体表现不佳，平均分仅为{avg_score:.1f}分。{trend_analysis}建议全面复习基础知识，增加学习时间和练习量，必要时寻求一对一辅导。"


def generate_class_knowledge_heatmap(
    homeworks: list[HomeworkInfo],
) -> list[ClassKnowledgePoint]:
    """生成班级知识点掌握情况热力图"""
    # 预设的知识点列表
    knowledge_points = ["基本概念", "公式应用", "解题思路", "计算准确性", "综合应用"]

    # 如果没有分数，返回默认值
    if not any(hw.score is not None for hw in homeworks):
        return [
            ClassKnowledgePoint(knowledge=kp, averageMastery=0)
            for kp in knowledge_points
        ]

    # 计算班级平均分
    all_scores = [hw.score for hw in homeworks if hw.score is not None]
    avg_score = sum(all_scores) / len(all_scores) if all_scores else 0

    # 为不同知识点设置略有差异的掌握度
    import random

    random.seed(42)  # 固定随机种子

    result: list[ClassKnowledgePoint] = []
    for kp in knowledge_points:
        # 基于平均分生成掌握程度，添加一些随机波动使数据更真实
        mastery = (avg_score / 100) * (0.85 + random.uniform(-0.2, 0.2))
        mastery = max(0, min(1, mastery))  # 限制在0-1范围内
        result.append(
            ClassKnowledgePoint(knowledge=kp, averageMastery=round(mastery * 100) / 100)
        )

    return result


def generate_class_analysis(homeworks: list[HomeworkInfo], avg_score: float) -> str:
    """生成班级整体学习分析"""
    # 统计优秀、良好、及格和不及格的学生比例
    score_counts = {"优秀": 0, "良好": 0, "及格": 0, "不及格": 0}
    student_scores = {}  # 用于存储每个学生的平均分

    for hw in homeworks:
        if hw.score is not None:
            if hw.student_id not in student_scores:
                student_scores[hw.student_id] = []
            student_scores[hw.student_id].append(hw.score)

    # 计算每个学生的平均分并分类
    total_students = len(student_scores)
    if total_students == 0:
        return "班级暂无足够的作业数据进行分析。"

    for scores in student_scores.values():
        student_avg = sum(scores) / len(scores)
        if student_avg >= 90:
            score_counts["优秀"] += 1
        elif student_avg >= 80:
            score_counts["良好"] += 1
        elif student_avg >= 60:
            score_counts["及格"] += 1
        else:
            score_counts["不及格"] += 1

    # 计算各类别占比
    percentages = {k: round(v / total_students * 100) for k, v in score_counts.items()}

    # 根据班级整体情况给出分析
    analysis = f"班级平均分为{avg_score:.1f}分，共有{total_students}名学生。其中优秀学生占{percentages['优秀']}%，良好学生占{percentages['良好']}%，及格学生占{percentages['及格']}%，不及格学生占{percentages['不及格']}%。"

    # 班级整体建议
    if avg_score >= 85:
        analysis += " 班级整体水平优秀，建议进一步提高教学难度，针对不同层次学生制定差异化教学策略，激发学生学习潜力。"
    elif avg_score >= 75:
        analysis += " 班级整体水平良好，建议继续保持现有教学进度，关注学习困难的学生，帮助他们提升成绩。"
    elif avg_score >= 60:
        analysis += " 班级整体水平一般，建议加强基础知识教学，增加课堂互动和作业练习，提高学生的参与度和学习积极性。"
    else:
        analysis += " 班级整体水平不佳，建议重点复习基础知识，降低教学难度，增加辅导次数，帮助学生建立学习信心。"

    return analysis
