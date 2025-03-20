import React from "react";
import { Card, Row, Col, Statistic, Space } from "antd";
import {
  UserOutlined,
  BookOutlined,
  FileOutlined,
  ClockCircleOutlined,
} from "@ant-design/icons";
// 需要先安装依赖: npm install --save echarts-for-react echarts
import ReactECharts from "echarts-for-react";

const DataAnalysis: React.FC = () => {
  // 示例数据，后续将通过API获取
  const statisticsData = {
    totalStudents: 0,
    totalLessons: 0,
    totalResources: 0,
    averageTime: 0,
  };

  // 学习进度图表配置
  const progressOption = {
    title: {
      text: "知识点掌握情况",
    },
    tooltip: {},
    radar: {
      indicator: [
        { name: "语言知识", max: 100 },
        { name: "文学常识", max: 100 },
        { name: "阅读能力", max: 100 },
        { name: "写作能力", max: 100 },
        { name: "口语表达", max: 100 },
      ],
    },
    series: [
      {
        type: "radar",
        data: [
          {
            value: [80, 75, 85, 70, 78],
            name: "班级平均水平",
          },
        ],
      },
    ],
  };

  // 学习时长分布图表配置
  const timeDistributionOption = {
    title: {
      text: "每周学习时长分布",
    },
    xAxis: {
      type: "category",
      data: ["周一", "周二", "周三", "周四", "周五", "周六", "周日"],
    },
    yAxis: {
      type: "value",
    },
    series: [
      {
        data: [30, 35, 40, 38, 42, 25, 20],
        type: "bar",
      },
    ],
  };

  return (
    <div style={{ padding: "24px" }}>
      <Row gutter={[16, 16]}>
        <Col span={6}>
          <Card bordered={false}>
            <Statistic
              title="学生总数"
              value={statisticsData.totalStudents}
              prefix={<UserOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card bordered={false}>
            <Statistic
              title="课程总数"
              value={statisticsData.totalLessons}
              prefix={<BookOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card bordered={false}>
            <Statistic
              title="资源数量"
              value={statisticsData.totalResources}
              prefix={<FileOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card bordered={false}>
            <Statistic
              title="平均学习时长（小时）"
              value={statisticsData.averageTime}
              prefix={<ClockCircleOutlined />}
            />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="学习进度分析" bordered={false}>
            <ReactECharts
              option={{
                title: {
                  text: "知识点掌握情况",
                },
                tooltip: {},
                radar: {
                  indicator: [
                    { name: "语言知识", max: 100 },
                    { name: "文学常识", max: 100 },
                    { name: "阅读能力", max: 100 },
                    { name: "写作能力", max: 100 },
                    { name: "口语表达", max: 100 },
                  ],
                },
                series: [
                  {
                    type: "radar" as const,
                    data: [
                      {
                        value: [80, 75, 85, 70, 78],
                        name: "班级平均水平",
                      },
                    ],
                  },
                ],
              }}
              style={{ height: "400px" }}
            />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="学习时长分布" bordered={false}>
            <ReactECharts
              option={{
                title: {
                  text: "每周学习时长分布",
                },
                xAxis: {
                  type: "category" as const,
                  data: [
                    "周一",
                    "周二",
                    "周三",
                    "周四",
                    "周五",
                    "周六",
                    "周日",
                  ],
                },
                yAxis: {
                  type: "value" as const,
                },
                series: [
                  {
                    data: [30, 35, 40, 38, 42, 25, 20],
                    type: "bar" as const,
                  },
                ],
              }}
              style={{ height: "400px" }}
            />
          </Card>
        </Col>
        <Col span={24}>
          <Card title="个性化学习建议" bordered={false}>
            <Space direction="vertical" style={{ width: "100%" }}>
              <p>1. 根据学生历史学习数据分析，建议重点关注以下知识点：</p>
              <ul>
                <li>语言知识部分：重点加强语法规则和词汇应用</li>
                <li>写作能力：建议增加实践练习，特别是议论文写作</li>
              </ul>
              <p>2. 学习方法建议：</p>
              <ul>
                <li>增加互动性学习活动，提高课堂参与度</li>
                <li>采用多样化的教学资源，如视频、图片等</li>
                <li>适当增加小组讨论环节，促进协作学习</li>
              </ul>
              <p>3. 资源推荐：</p>
              <ul>
                <li>推荐观看相关主题的微课视频</li>
                <li>建议使用在线练习平台进行针对性训练</li>
                <li>提供补充阅读材料，拓展知识面</li>
              </ul>
            </Space>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default DataAnalysis;
