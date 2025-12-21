import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import { Layout, Menu } from 'antd';
import { HomeOutlined, HeartOutlined, RobotOutlined } from '@ant-design/icons';
import JobList from './components/JobList';
import JobDetail from './components/JobDetail';
import FavoriteList from './components/FavoriteList';
import ScraperPanel from './components/ScraperPanel';
import './App.css';

const { Header, Content, Footer } = Layout;

function App() {
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ display: 'flex', alignItems: 'center' }}>
        <div style={{ color: 'white', fontSize: '20px', marginRight: '50px' }}>
          就业信息查询系统
        </div>
        <Menu
          theme="dark"
          mode="horizontal"
          defaultSelectedKeys={['1']}
          style={{ flex: 1, minWidth: 0 }}
        >
          <Menu.Item key="1" icon={<HomeOutlined />}>
            <Link to="/">职位列表</Link>
          </Menu.Item>
          <Menu.Item key="2" icon={<HeartOutlined />}>
            <Link to="/favorites">我的收藏</Link>
          </Menu.Item>
          <Menu.Item key="3" icon={<RobotOutlined />}>
            <Link to="/scraper">爬虫管理</Link>
          </Menu.Item>
        </Menu>
      </Header>
      <Content style={{ padding: '24px 50px' }}>
        <Routes>
          <Route path="/" element={<JobList />} />
          <Route path="/job/:id" element={<JobDetail />} />
          <Route path="/favorites" element={<FavoriteList />} />
          <Route path="/scraper" element={<ScraperPanel />} />
        </Routes>
      </Content>
      <Footer style={{ textAlign: 'center' }}>
        就业信息查询系统 © 2025
      </Footer>
    </Layout>
  );
}

export default App;
