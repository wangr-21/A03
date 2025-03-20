import React from "react";
import { Layout, Menu } from "antd";
import { Routes, Route, Link } from "react-router-dom";
import {
  BookOutlined,
  DatabaseOutlined,
  BarChartOutlined,
} from "@ant-design/icons";
import TeacherWorkbench from "./components/TeacherWorkbench";
import ResourceCenter from "./components/ResourceCenter";
import DataAnalysis from "./components/DataAnalysis";

const { Header, Content, Sider } = Layout;

const App: React.FC = () => {
  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Header style={{ display: "flex", alignItems: "center" }}>
        <h1 style={{ color: "#fff", margin: 0 }}>智能备课助手</h1>
      </Header>
      <Layout>
        <Sider width={200}>
          <Menu
            mode="inline"
            style={{ height: "100%", borderRight: 0 }}
            defaultSelectedKeys={["1"]}
          >
            <Menu.Item key="1" icon={<BookOutlined />}>
              <Link to="/workbench">教师工作台</Link>
            </Menu.Item>
            <Menu.Item key="2" icon={<DatabaseOutlined />}>
              <Link to="/resources">资源中心</Link>
            </Menu.Item>
            <Menu.Item key="3" icon={<BarChartOutlined />}>
              <Link to="/analysis">数据分析</Link>
            </Menu.Item>
          </Menu>
        </Sider>
        <Layout style={{ padding: "24px" }}>
          <Content
            style={{
              background: "#fff",
              padding: 24,
              margin: 0,
              minHeight: 280,
            }}
          >
            <Routes>
              <Route path="/workbench" element={<TeacherWorkbench />} />
              <Route path="/resources" element={<ResourceCenter />} />
              <Route path="/analysis" element={<DataAnalysis />} />
              <Route path="/" element={<div>欢迎使用智能备课助手</div>} />
            </Routes>
          </Content>
        </Layout>
      </Layout>
    </Layout>
  );
};

export default App;
