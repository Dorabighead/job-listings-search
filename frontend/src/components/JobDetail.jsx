import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Descriptions, Tag, Button, Space, message } from 'antd';
import { ArrowLeftOutlined, HeartOutlined, HeartFilled, LinkOutlined } from '@ant-design/icons';
import { jobAPI, favoriteAPI } from '../services/api';

function JobDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isFavorite, setIsFavorite] = useState(false);

  useEffect(() => {
    fetchJobDetail();
  }, [id]);

  const fetchJobDetail = async () => {
    setLoading(true);
    try {
      const response = await jobAPI.getJob(id);
      setJob(response.data);
    } catch (error) {
      message.error('获取职位详情失败');
    } finally {
      setLoading(false);
    }
  };

  const handleFavorite = async () => {
    try {
      if (isFavorite) {
        message.info('该职位已收藏');
      } else {
        await favoriteAPI.addFavorite({ job_id: parseInt(id) });
        setIsFavorite(true);
        message.success('收藏成功');
      }
    } catch (error) {
      message.error('操作失败');
    }
  };

  if (!job) return null;

  return (
    <div>
      <Space style={{ marginBottom: '16px' }}>
        <Button icon={<ArrowLeftOutlined />} onClick={() => navigate('/')}>
          返回列表
        </Button>
        <Button
          type="primary"
          icon={isFavorite ? <HeartFilled /> : <HeartOutlined />}
          onClick={handleFavorite}
        >
          {isFavorite ? '已收藏' : '收藏'}
        </Button>
        {job.url && (
          <Button
            icon={<LinkOutlined />}
            onClick={() => window.open(job.url, '_blank')}
          >
            查看原始链接
          </Button>
        )}
      </Space>

      <Card title={<h2>{job.title}</h2>}>
        <Descriptions column={2} bordered>
          <Descriptions.Item label="公司">{job.company}</Descriptions.Item>
          <Descriptions.Item label="薪资">
            <span style={{ color: '#ff4d4f', fontWeight: 'bold', fontSize: '16px' }}>
              {job.salary_min && job.salary_max
                ? `¥${job.salary_min / 1000}k - ${job.salary_max / 1000}k`
                : '薪资面议'}
            </span>
          </Descriptions.Item>
          <Descriptions.Item label="地点">{job.location}</Descriptions.Item>
          <Descriptions.Item label="经验要求">{job.experience}</Descriptions.Item>
          <Descriptions.Item label="学历要求">{job.education}</Descriptions.Item>
          <Descriptions.Item label="工作类型">{job.job_type}</Descriptions.Item>
          <Descriptions.Item label="数据来源">
            <Tag color="blue">{job.source}</Tag>
          </Descriptions.Item>
          <Descriptions.Item label="发布时间">
            {new Date(job.created_at).toLocaleString('zh-CN')}
          </Descriptions.Item>
        </Descriptions>

        {job.welfare && (
          <div style={{ marginTop: '24px' }}>
            <h3>福利待遇</h3>
            <div>
              {job.welfare.split(',').map((w, i) => (
                <Tag key={i} color="green" style={{ marginBottom: '8px' }}>
                  {w.trim()}
                </Tag>
              ))}
            </div>
          </div>
        )}

        <div style={{ marginTop: '24px' }}>
          <h3>职位描述</h3>
          <p style={{ whiteSpace: 'pre-wrap' }}>{job.description}</p>
        </div>

        {job.requirements && job.requirements !== job.description && (
          <div style={{ marginTop: '24px' }}>
            <h3>任职要求</h3>
            <p style={{ whiteSpace: 'pre-wrap' }}>{job.requirements}</p>
          </div>
        )}
      </Card>
    </div>
  );
}

export default JobDetail;
