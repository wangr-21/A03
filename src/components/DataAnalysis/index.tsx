import React, { useState, useEffect } from "react";
import { Layout, Card, Row, Col, Statistic, Spin, message } from "antd";
import {
  UserOutlined,
  BookOutlined,
  CheckCircleOutlined,
  RiseOutlined,
} from "@ant-design/icons";

const { Content } = Layout;

const DataAnalysis: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [analysisData, setAnalysisData] = useState([
    {
      title: "学习能力评估",
      value: 0,
      icon: <UserOutlined style={{ fontSize: "24px" }} />,
      prefix: "分",
      color: "#1890ff",
    },
    {
      title: "知识点掌握度",
      value: 0,
      icon: <BookOutlined style={{ fontSize: "24px" }} />,
      prefix: "%",
      color: "#52c41a",
    },
    {
      title: "完成任务数",
      value: 0,
      icon: <CheckCircleOutlined style={{ fontSize: "24px" }} />,
      prefix: "个",
      color: "#722ed1",
    },
    {
      title: "学习进度",
      value: 0,
      icon: <RiseOutlined style={{ fontSize: "24px" }} />,
      prefix: "%",
      color: "#fa8c16",
    },
  ]);

  useEffect(() => {
    fetchAnalysisData();
  }, []);

  const fetchAnalysisData = async () => {
    try {
      const response = await fetch("/api/ai/analysis-data");
      if (!response.ok) {
        throw new Error("获取分析数据失败");
      }
      const data = await response.json();
      setAnalysisData((prev) =>
        prev.map((item, index) => ({
          ...item,
          value: data[index].value,
        }))
      );
    } catch (error) {
      message.error("获取学情分析数据失败，请重试");
      console.error("获取分析数据错误:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout style={{ padding: "24px" }}>
      <Content>
        <Spin spinning={loading}>
          <Row gutter={[24, 24]}>
            {analysisData.map((data, index) => (
              <Col span={6} key={index}>
                <Card>
                  <Statistic
                    title={data.title}
                    value={data.value}
                    prefix={data.icon}
                    suffix={data.prefix}
                    valueStyle={{ color: data.color }}
                  />
                </Card>
              </Col>
            ))}
          </Row>
        </Spin>
      </Content>
    </Layout>
  );
};

export default DataAnalysis;
