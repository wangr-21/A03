import React from "react";
import { Card, Row, Col, Button, Space } from "antd";
import {
  FileAddOutlined,
  PictureOutlined,
  FormOutlined,
  AreaChartOutlined,
} from "@ant-design/icons";

const Workbench: React.FC = () => {
  return (
    <div style={{ padding: "24px" }}>
      <Row gutter={[16, 16]}>
        <Col span={24}>
          <Card title="快速操作" bordered={false}>
            <Space size="large">
              <Button type="primary" icon={<FileAddOutlined />} size="large">
                创建教案
              </Button>
              <Button icon={<PictureOutlined />} size="large">
                生成资源
              </Button>
              <Button icon={<FormOutlined />} size="large">
                生成练习
              </Button>
              <Button icon={<AreaChartOutlined />} size="large">
                学情分析
              </Button>
            </Space>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="最近教案" bordered={false}>
            {/* 最近教案列表将在这里实现 */}
            <p>暂无最近教案</p>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="教学资源" bordered={false}>
            {/* 教学资源列表将在这里实现 */}
            <p>暂无教学资源</p>
          </Card>
        </Col>
        <Col span={24}>
          <Card title="教学数据概览" bordered={false}>
            {/* 数据统计图表将在这里实现 */}
            <p>暂无数据统计</p>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Workbench;
