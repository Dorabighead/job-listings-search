import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Row, Col, Input, Select, Button, Pagination, message, Tag, Space } from 'antd';
import { SearchOutlined, HeartOutlined, HeartFilled, DownloadOutlined } from '@ant-design/icons';
import { jobAPI, favoriteAPI } from '../services/api';

const { Search } = Input;
const { Option } = Select;

function JobList() {
  const navigate = useNavigate();
  const [jobs, setJobs] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [limit] = useState(20);
  const [favorites, setFavorites] = useState(new Set());

  const [filters, setFilters] = useState({
    keyword: '',
    location: '',
    source: '',
  });

  useEffect(() => {
    fetchJobs();
    fetchFavorites();
  }, [page, filters]);

  const fetchJobs = async () => {
    setLoading(true);
    try {
      const params = {
        skip: (page - 1) * limit,
        limit,
        ...filters,
      };
      const response = await jobAPI.getJobs(params);
      setJobs(response.data.jobs);
      setTotal(response.data.total);
    } catch (error) {
      message.error('获取职位列表失败');
    } finally {
      setLoading(false);
    }
  };

  const fetchFavorites = async () => {
    try {
      const response = await favoriteAPI.getFavorites();
      const favJobIds = new Set(response.data.map(fav => fav.job_id));
      setFavorites(favJobIds);
    } catch (error) {
      console.error('获取收藏失败', error);
    }
  };

  const handleSearch = (value) => {
    setFilters({ ...filters, keyword: value });
    setPage(1);
  };

  const handleLocationChange = (value) => {
    setFilters({ ...filters, location: value });
    setPage(1);
  };

  const handleSourceChange = (value) => {
    setFilters({ ...filters, source: value });
    setPage(1);
  };

  const handleFavorite = async (e, jobId) => {
    e.stopPropagation();
    try {
      if (favorites.has(jobId)) {
        message.info('该职位已在收藏中');
      } else {
        await favoriteAPI.addFavorite({ job_id: jobId });
        setFavorites(new Set([...favorites, jobId]));
        message.success('收藏成功');
      }
    } catch (error) {
      message.error('操作失败');
    }
  };

  const handleExport = async () => {
    try {
      const response = await jobAPI.exportExcel(filters);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'jobs.xlsx');
      document.body.appendChild(link);
      link.click();
      link.remove();
      message.success('导出成功');
    } catch (error) {
      message.error('导出失败');
    }
  };

  return (
    <div>
      <div className="filter-panel">
        <Space size="large" style={{ width: '100%' }} direction="vertical">
          <Row gutter={16}>
            <Col span={12}>
              <Search
                placeholder="搜索职位、公司"
                enterButton={<SearchOutlined />}
                size="large"
                onSearch={handleSearch}
              />
            </Col>
            <Col span={6}>
              <Select
                placeholder="选择地点"
                size="large"
                style={{ width: '100%' }}
                onChange={handleLocationChange}
                allowClear
              >
                <Option value="">全部</Option>
                <Option value="北京">北京</Option>
                <Option value="上海">上海</Option>
                <Option value="广州">广州</Option>
                <Option value="深圳">深圳</Option>
                <Option value="杭州">杭州</Option>
              </Select>
            </Col>
            <Col span={6}>
              <Select
                placeholder="数据来源"
                size="large"
                style={{ width: '100%' }}
                onChange={handleSourceChange}
                allowClear
              >
                <Option value="">全部</Option>
                <Option value="boss">Boss直聘</Option>
                <Option value="zhaopin">智联招聘</Option>
                <Option value="51job">前程无忧</Option>
                <Option value="lagou">拉勾网</Option>
              </Select>
            </Col>
          </Row>
          <Button
            type="primary"
            icon={<DownloadOutlined />}
            onClick={handleExport}
          >
            导出Excel
          </Button>
        </Space>
      </div>

      <Row gutter={[16, 16]}>
        {jobs.map((job) => (
          <Col span={24} key={job.id}>
            <Card
              className="job-card"
              hoverable
              onClick={() => navigate(`/job/${job.id}`)}
              extra={
                <Button
                  type="text"
                  icon={favorites.has(job.id) ? <HeartFilled style={{ color: '#ff4d4f' }} /> : <HeartOutlined />}
                  onClick={(e) => handleFavorite(e, job.id)}
                />
              }
            >
              <Row justify="space-between" align="middle">
                <Col span={16}>
                  <h3>{job.title}</h3>
                  <p>{job.company}</p>
                  <Space>
                    <Tag>{job.location}</Tag>
                    <Tag>{job.experience}</Tag>
                    <Tag>{job.education}</Tag>
                    <Tag color="blue">{job.source}</Tag>
                  </Space>
                </Col>
                <Col span={8} style={{ textAlign: 'right' }}>
                  <div className="salary">
                    {job.salary_min && job.salary_max
                      ? `¥${job.salary_min / 1000}k - ${job.salary_max / 1000}k`
                      : '薪资面议'}
                  </div>
                </Col>
              </Row>
            </Card>
          </Col>
        ))}
      </Row>

      <div style={{ marginTop: '24px', textAlign: 'center' }}>
        <Pagination
          current={page}
          total={total}
          pageSize={limit}
          onChange={(page) => setPage(page)}
          showSizeChanger={false}
          showTotal={(total) => `共 ${total} 条`}
        />
      </div>
    </div>
  );
}

export default JobList;
