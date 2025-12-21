import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Row, Col, Button, message, Tag, Space, Input, Modal } from 'antd';
import { DeleteOutlined, EditOutlined, EyeOutlined } from '@ant-design/icons';
import { favoriteAPI } from '../services/api';

const { TextArea } = Input;

function FavoriteList() {
  const navigate = useNavigate();
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(false);
  const [editModal, setEditModal] = useState({ visible: false, id: null, note: '' });

  useEffect(() => {
    fetchFavorites();
  }, []);

  const fetchFavorites = async () => {
    setLoading(true);
    try {
      const response = await favoriteAPI.getFavorites();
      setFavorites(response.data);
    } catch (error) {
      message.error('获取收藏列表失败');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      await favoriteAPI.deleteFavorite(id);
      message.success('取消收藏成功');
      fetchFavorites();
    } catch (error) {
      message.error('操作失败');
    }
  };

  const handleEditNote = (favorite) => {
    setEditModal({
      visible: true,
      id: favorite.id,
      note: favorite.note || ''
    });
  };

  const handleSaveNote = async () => {
    try {
      await favoriteAPI.updateFavorite(editModal.id, { note: editModal.note });
      message.success('备注更新成功');
      setEditModal({ visible: false, id: null, note: '' });
      fetchFavorites();
    } catch (error) {
      message.error('更新失败');
    }
  };

  return (
    <div>
      <h2>我的收藏 ({favorites.length})</h2>

      <Row gutter={[16, 16]}>
        {favorites.map((favorite) => {
          const job = favorite.job;
          return (
            <Col span={24} key={favorite.id}>
              <Card
                className="job-card"
                actions={[
                  <Button
                    type="text"
                    icon={<EyeOutlined />}
                    onClick={() => navigate(`/job/${job.id}`)}
                  >
                    查看详情
                  </Button>,
                  <Button
                    type="text"
                    icon={<EditOutlined />}
                    onClick={() => handleEditNote(favorite)}
                  >
                    编辑备注
                  </Button>,
                  <Button
                    type="text"
                    danger
                    icon={<DeleteOutlined />}
                    onClick={() => handleDelete(favorite.id)}
                  >
                    取消收藏
                  </Button>,
                ]}
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
                    {favorite.note && (
                      <div style={{ marginTop: '12px', padding: '8px', background: '#f5f5f5', borderRadius: '4px' }}>
                        <strong>备注：</strong>{favorite.note}
                      </div>
                    )}
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
          );
        })}
      </Row>

      <Modal
        title="编辑收藏备注"
        open={editModal.visible}
        onOk={handleSaveNote}
        onCancel={() => setEditModal({ visible: false, id: null, note: '' })}
      >
        <TextArea
          rows={4}
          value={editModal.note}
          onChange={(e) => setEditModal({ ...editModal, note: e.target.value })}
          placeholder="添加备注信息..."
        />
      </Modal>
    </div>
  );
}

export default FavoriteList;
