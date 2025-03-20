import React, { useState } from "react";
import {
  Layout,
  Menu,
  Card,
  Form,
  Input,
  Button,
  Select,
  Space,
  message,
} from "antd";
import {
  BookOutlined,
  FormOutlined,
  InteractionOutlined,
} from "@ant-design/icons";
import api from "../../api";

const { Content, Sider } = Layout;
const { TextArea } = Input;
const { Option } = Select;

const TeacherWorkbench: React.FC = () => {
  const [selectedKey, setSelectedKey] = useState("1");
  const [lessonPlan, setLessonPlan] = useState<string>("");

  const handleGenerateLesson = async (values: any) => {
    try {
      message.loading({ content: "正在生成教案...", key: "lessonPlan" });
      const response = await api.generateTeachingPlan(
        values.subject,
        values.grade,
        values.chapter
      );

      if (response.success) {
        message.success({ content: "教案生成成功！", key: "lessonPlan" });
        setLessonPlan(response.data);
      } else {
        throw new Error("生成教案失败");
      }
    } catch (error) {
      message.error({ content: "生成教案失败，请重试", key: "lessonPlan" });
      console.error("生成教案错误:", error);
    }
  };

  const handleGenerateImage = async () => {
    try {
      message.loading({ content: "正在生成图片...", key: "image" });
      const response = await api.generateTeachingImage("教学相关的图片");
      if (response.success) {
        message.success({ content: "图片生成成功！", key: "image" });
        // TODO: 处理生成的图片URL
      } else {
        throw new Error("生成图片失败");
      }
    } catch (error) {
      message.error({ content: "生成图片失败，请重试", key: "image" });
      console.error("生成图片错误:", error);
    }
  };

  const handleGenerateVideo = async () => {
    message.info("视频生成功能正在开发中...");
  };

  const handleGenerateExercise = async () => {
    message.info("练习题生成功能正在开发中...");
  };

  const renderContent = () => {
    switch (selectedKey) {
      case "1":
        return (
          <Card title="智能教案生成" bordered={false}>
            <Form layout="vertical" onFinish={handleGenerateLesson}>
              <Form.Item
                name="subject"
                label="学科"
                rules={[{ required: true }]}
              >
                <Select placeholder="请选择学科">
                  <Option value="chinese">语文</Option>
                  <Option value="math">数学</Option>
                  <Option value="english">英语</Option>
                </Select>
              </Form.Item>
              <Form.Item name="grade" label="年级" rules={[{ required: true }]}>
                <Select placeholder="请选择年级">
                  <Option value="7">初一</Option>
                  <Option value="8">初二</Option>
                  <Option value="9">初三</Option>
                </Select>
              </Form.Item>
              <Form.Item
                name="chapter"
                label="教学内容"
                rules={[{ required: true }]}
              >
                <TextArea rows={4} placeholder="请输入本节课的教学内容" />
              </Form.Item>
              <Form.Item
                name="objectives"
                label="教学目标"
                rules={[{ required: true }]}
              >
                <TextArea rows={4} placeholder="请输入教学目标" />
              </Form.Item>
              <Form.Item>
                <Button type="primary" htmlType="submit">
                  生成教案
                </Button>
              </Form.Item>
            </Form>
            {lessonPlan && (
              <Card title="生成的教案" style={{ marginTop: 16 }}>
                <pre style={{ whiteSpace: "pre-wrap" }}>{lessonPlan}</pre>
              </Card>
            )}
          </Card>
        );
      case "2":
        return (
          <Card title="互动环节设计" bordered={false}>
            <Form layout="vertical">
              <Form.Item name="activityType" label="互动类型">
                <Select placeholder="请选择互动类型">
                  <Option value="discussion">分组讨论</Option>
                  <Option value="game">教学游戏</Option>
                  <Option value="quiz">课堂测验</Option>
                </Select>
              </Form.Item>
              <Form.Item name="duration" label="时长(分钟)">
                <Input type="number" />
              </Form.Item>
              <Form.Item name="description" label="活动描述">
                <TextArea rows={4} placeholder="请描述互动活动的具体内容" />
              </Form.Item>
              <Form.Item>
                <Button type="primary">生成互动方案</Button>
              </Form.Item>
            </Form>
          </Card>
        );
      case "3":
        return (
          <Card title="教学资源库" bordered={false}>
            <Space direction="vertical" style={{ width: "100%" }}>
              <Card type="inner" title="推荐资源">
                <p>1. 教学PPT模板</p>
                <p>2. 课堂互动游戏素材</p>
                <p>3. 知识点讲解视频</p>
                <p>4. 练习题资源包</p>
              </Card>
              <Card type="inner" title="资源生成">
                <Space>
                  <Button onClick={handleGenerateImage}>生成图片资源</Button>
                  <Button onClick={handleGenerateVideo}>生成视频资源</Button>
                  <Button onClick={handleGenerateExercise}>生成练习题</Button>
                </Space>
              </Card>
            </Space>
          </Card>
        );
      default:
        return null;
    }
  };

  return (
    <Layout style={{ height: "100vh" }}>
      <Sider width={200} theme="light">
        <Menu
          mode="inline"
          selectedKeys={[selectedKey]}
          onSelect={({ key }) => setSelectedKey(key)}
          style={{ height: "100%", borderRight: 0 }}
        >
          <Menu.Item key="1" icon={<FormOutlined />}>
            智能教案生成
          </Menu.Item>
          <Menu.Item key="2" icon={<InteractionOutlined />}>
            互动环节设计
          </Menu.Item>
          <Menu.Item key="3" icon={<BookOutlined />}>
            教学资源库
          </Menu.Item>
        </Menu>
      </Sider>
      <Content style={{ padding: "24px", minHeight: 280 }}>
        {renderContent()}
      </Content>
    </Layout>
  );
};

export default TeacherWorkbench;
