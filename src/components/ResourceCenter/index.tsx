import React, { useState } from "react";
import {
  Layout,
  Card,
  Row,
  Col,
  Button,
  Space,
  Form,
  Input,
  Select,
  Upload,
  message,
} from "antd";
import {
  PictureOutlined,
  VideoCameraOutlined,
  FileTextOutlined,
  QuestionCircleOutlined,
  UploadOutlined,
} from "@ant-design/icons";

const { Content } = Layout;
const { TextArea } = Input;
const { Option } = Select;

const ResourceCenter: React.FC = () => {
  const [generatedResources, setGeneratedResources] = useState<
    {
      type: string;
      data: {
        url: string;
      };
    }[]
  >([]);

  const handleGenerateResource = async (type: string, values: object) => {
    try {
      message.loading({ content: `正在生成${type}资源...`, key: "resource" });
      const response = await fetch(`/api/ai/generate-${type.toLowerCase()}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(values),
      });

      if (!response.ok) {
        throw new Error(`生成${type}资源失败`);
      }

      const data = await response.json();
      message.success({ content: `${type}资源生成成功！`, key: "resource" });
      setGeneratedResources((prev) => [...prev, { type, data }]);
    } catch (error) {
      message.error({
        content: `生成${type}资源失败，请重试`,
        key: "resource",
      });
      console.error(`生成${type}资源错误:`, error);
    }
  };

  const resourceTypes = [
    {
      title: "图片资源生成",
      icon: <PictureOutlined style={{ fontSize: "24px" }} />,
      content: (
        <Form
          layout="vertical"
          onFinish={(values: {
            imageType: "concept" | "mindmap" | "scene";
            description: string;
          }) => handleGenerateResource("图片", values)}
        >
          <Form.Item
            name="imageType"
            label="图片类型"
            rules={[{ required: true }]}
          >
            <Select placeholder="请选择图片类型">
              <Option value="concept">教学概念可视化</Option>
              <Option value="mindmap">思维导图</Option>
              <Option value="scene">教学情境插图</Option>
            </Select>
          </Form.Item>
          <Form.Item
            name="description"
            label="图片描述"
            rules={[{ required: true }]}
          >
            <TextArea rows={4} placeholder="请描述您需要的图片内容" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit">
              生成图片
            </Button>
          </Form.Item>
        </Form>
      ),
    },
    {
      title: "视频资源生成",
      icon: <VideoCameraOutlined style={{ fontSize: "24px" }} />,
      content: (
        <Form
          layout="vertical"
          onFinish={(values: {
            videoType: "micro" | "animation" | "experiment";
            script: string;
          }) => handleGenerateResource("视频", values)}
        >
          <Form.Item
            name="videoType"
            label="视频类型"
            rules={[{ required: true }]}
          >
            <Select placeholder="请选择视频类型">
              <Option value="micro">微课视频</Option>
              <Option value="animation">教学动画</Option>
              <Option value="experiment">实验演示</Option>
            </Select>
          </Form.Item>
          <Form.Item
            name="script"
            label="视频脚本"
            rules={[{ required: true }]}
          >
            <TextArea rows={4} placeholder="请输入视频内容脚本" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit">
              生成视频
            </Button>
          </Form.Item>
        </Form>
      ),
    },
  ];

  return (
    <Layout style={{ padding: "24px" }}>
      <Content>
        <Row gutter={[24, 24]}>
          {resourceTypes.map((type, index) => (
            <Col span={12} key={index}>
              <Card title={type.title} extra={type.icon}>
                {type.content}
              </Card>
            </Col>
          ))}
        </Row>
        {generatedResources.length > 0 && (
          <Card title="生成的资源" style={{ marginTop: "24px" }}>
            <Row gutter={[16, 16]}>
              {generatedResources.map((resource, index) => (
                <Col span={8} key={index}>
                  <Card
                    size="small"
                    title={`${resource.type}资源 ${index + 1}`}
                  >
                    {/* 根据资源类型展示不同的预览内容 */}
                    {resource.type === "图片" && (
                      <img
                        src={resource.data.url}
                        alt="生成的图片"
                        style={{ width: "100%" }}
                      />
                    )}
                    {resource.type === "视频" && (
                      <video
                        src={resource.data.url}
                        controls
                        style={{ width: "100%" }}
                      />
                    )}
                  </Card>
                </Col>
              ))}
            </Row>
          </Card>
        )}
      </Content>
    </Layout>
  );
};

export default ResourceCenter;
