import React from "react";
import { Card, Row, Col, List, Tag, Button, Space } from "antd";
import {
  PictureOutlined,
  VideoCameraOutlined,
  FileTextOutlined,
  UploadOutlined,
} from "@ant-design/icons";

interface ResourceItem {
  id: string;
  title: string;
  type: "image" | "video" | "document";
  createTime: string;
  tags: string[];
}

const ResourceCenter: React.FC = () => {
  // 示例数据，后续将通过API获取
  const resources: ResourceItem[] = [];

  const getIconByType = (type: string) => {
    switch (type) {
      case "image":
        return <PictureOutlined />;
      case "video":
        return <VideoCameraOutlined />;
      default:
        return <FileTextOutlined />;
    }
  };

  const getTypeText = (type: string) => {
    const typeMap = {
      image: "图片",
      video: "视频",
      document: "文档",
    };
    return typeMap[type as keyof typeof typeMap] || "其他";
  };

  return (
    <div style={{ padding: "24px" }}>
      <Row gutter={[16, 16]}>
        <Col span={24}>
          <Card bordered={false}>
            <Space style={{ marginBottom: 16 }}>
              <Button type="primary" icon={<UploadOutlined />}>
                上传资源
              </Button>
              <Button icon={<PictureOutlined />}>生成图片</Button>
              <Button icon={<VideoCameraOutlined />}>生成视频</Button>
            </Space>
            <List
              itemLayout="horizontal"
              dataSource={resources}
              locale={{ emptyText: "暂无资源" }}
              renderItem={(item) => (
                <List.Item
                  actions={[
                    <Button key="edit" type="link">
                      编辑
                    </Button>,
                    <Button key="delete" type="link" danger>
                      删除
                    </Button>,
                  ]}
                >
                  <List.Item.Meta
                    avatar={getIconByType(item.type)}
                    title={item.title}
                    description={
                      <Space>
                        <Tag color="blue">{getTypeText(item.type)}</Tag>
                        {item.tags.map((tag) => (
                          <Tag key={tag}>{tag}</Tag>
                        ))}
                        <span>创建时间：{item.createTime}</span>
                      </Space>
                    }
                  />
                </List.Item>
              )}
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default ResourceCenter;
