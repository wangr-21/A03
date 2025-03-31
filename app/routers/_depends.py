from typing import Annotated

from fastapi import Depends, HTTPException

from ..db import DBSession, StudentInfo


async def student_from_id(db: DBSession, student_id: str):
    """根据学号获取学生信息"""
    if (student := await db.get(StudentInfo, student_id)) is None:
        raise HTTPException(status_code=404, detail="未找到该学生")
    return student


StudentFromId = Annotated[StudentInfo, Depends(student_from_id)]
"""
依赖注入类型: 根据学号获取学生信息

- 路由函数使用需要参数中存在 student_id: str 字段
- 自动从请求中提取 student_id 参数, 查询数据库获取学生信息
"""
