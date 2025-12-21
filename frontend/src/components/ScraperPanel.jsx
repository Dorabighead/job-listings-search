import React, { useState, useEffect } from 'react';
import { Card, Form, Input, Select, Button, message, Progress, Alert, Space } from 'antd';
import { PlayCircleOutlined, SyncOutlined } from '@ant-design/icons';
import { scraperAPI } from '../services/api';

const { Option } = Select;

function ScraperPanel() {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(null);
  const [polling, setPolling] = useState(false);

  useEffect(() => {
    fetchStatus();
  }, []);

  useEffect(() => {
    let interval;
    if (polling) {
      interval = setInterval(fetchStatus, 2000);
    }
    return () => clearInterval(interval);
  }, [polling]);

  const fetchStatus = async () => {
    try {
      const response = await scraperAPI.getStatus();
      setStatus(response.data);
      if (response.data.running) {
        setPolling(true);
      } else {
        setPolling(false);
      }
    } catch (error) {
      console.error('获取状态失败', error);
    }
  };

  const handleSubmit = async (values) => {
    setLoading(true);
    try {
      await scraperAPI.runScraper(values);
      message.success('爬虫任务已启动');
      setPolling(true);
      form.resetFields();
    } catch (error) {
      message.error(error.response?.data?.detail || '启动失败');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>爬虫管理</h2>

      {status && status.running && (
        <Alert
          message="爬虫运行中"
          description={
            <Space direction="vertical" style={{ width: '100%' }}>
              <div>当前源: {status.current_source}</div>
              <div>已爬取: {status.jobs_scraped} 条职位</div>
              <Progress percent={100} status="active" showInfo={false} />
            </Space>
          }
          type="info"
          style={{ marginBottom: '24px' }}
        />
      )}

      {status && !status.running && status.message && (
        <Alert
          message="上次爬取结果"
          description={status.message}
          type="success"
          closable
          style={{ marginBottom: '24px' }}
        />
      )}

      <Card title="启动爬虫任务">
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          initialValues={{ source: 'boss', pages: 1 }}
        >
          <Form.Item
            label="数据来源"
            name="source"
            rules={[{ required: true, message: '请选择数据来源' }]}
          >
            <Select size="large">
              <Option value="boss">Boss直聘（已实现）</Option>
              <Option value="zhaopin" disabled>智联招聘（待实现）</Option>
              <Option value="51job" disabled>前程无忧（待实现）</Option>
              <Option value="lagou" disabled>拉勾网（待实现）</Option>
              <Option value="all" disabled>全部网站（待实现）</Option>
            </Select>
          </Form.Item>

          <Form.Item
            label="搜索关键词"
            name="keyword"
            rules={[{ required: true, message: '请输入搜索关键词' }]}
          >
            <Input size="large" placeholder="例如：Python、前端开发" />
          </Form.Item>

          <Form.Item
            label="工作地点"
            name="location"
          >
            <Select size="large" allowClear placeholder="选择地点（可选）">
              <Option value="北京">北京</Option>
              <Option value="上海">上海</Option>
              <Option value="广州">广州</Option>
              <Option value="深圳">深圳</Option>
              <Option value="杭州">杭州</Option>
              <Option value="成都">成都</Option>
              <Option value="武汉">武汉</Option>
            </Select>
          </Form.Item>

          <Form.Item
            label="爬取页数"
            name="pages"
            rules={[{ required: true, message: '请输入爬取页数' }]}
          >
            <Input type="number" min={1} max={10} size="large" />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={loading}
              disabled={status?.running}
              icon={<PlayCircleOutlined />}
              size="large"
              block
            >
              {status?.running ? '爬虫运行中...' : '启动爬虫'}
            </Button>
          </Form.Item>
        </Form>

        <Alert
          message="提示"
          description="爬虫将按照设定的参数自动爬取招聘网站数据。请合理控制爬取频率，避免对目标网站造成压力。建议每次爬取间隔5分钟以上。"
          type="warning"
          showIcon
        />
      </Card>
    </div>
  );
}

export default ScraperPanel;
