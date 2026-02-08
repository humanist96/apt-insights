'use client';

import { useState } from 'react';
import { EventItem, EventType } from '@/types/analysis';

interface EventManagerProps {
  events: EventItem[];
  onAdd: (event: Omit<EventItem, 'id'>) => void;
  onUpdate: (id: string, updates: Partial<EventItem>) => void;
  onDelete: (id: string) => void;
  onResetDefaults: () => void;
}

const EVENT_TYPES: Array<{ value: EventType; label: string; icon: string; color: string }> = [
  { value: '정책발표', label: '정책발표', icon: '📋', color: 'blue' },
  { value: '금리변동', label: '금리변동', icon: '📈', color: 'green' },
  { value: '재건축', label: '재건축', icon: '🏗️', color: 'purple' },
  { value: '입주시작', label: '입주시작', icon: '🏘️', color: 'orange' },
  { value: '기타', label: '기타', icon: '📌', color: 'gray' },
];

export default function EventManager({
  events,
  onAdd,
  onUpdate,
  onDelete,
  onResetDefaults,
}: EventManagerProps) {
  const [isAdding, setIsAdding] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    date: '',
    description: '',
    type: '정책발표' as EventType,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.name || !formData.date) {
      return;
    }

    if (editingId) {
      onUpdate(editingId, formData);
      setEditingId(null);
    } else {
      onAdd(formData);
    }

    setFormData({
      name: '',
      date: '',
      description: '',
      type: '정책발표',
    });
    setIsAdding(false);
  };

  const handleEdit = (event: EventItem) => {
    setFormData({
      name: event.name,
      date: event.date,
      description: event.description,
      type: event.type,
    });
    setEditingId(event.id);
    setIsAdding(true);
  };

  const handleCancel = () => {
    setFormData({
      name: '',
      date: '',
      description: '',
      type: '정책발표',
    });
    setEditingId(null);
    setIsAdding(false);
  };

  const getEventTypeConfig = (type: EventType) => {
    return EVENT_TYPES.find((t) => t.value === type) || EVENT_TYPES[4];
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">이벤트 관리</h3>
        <div className="flex gap-2">
          <button
            onClick={onResetDefaults}
            className="px-3 py-1.5 text-sm text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
          >
            기본값 복원
          </button>
          {!isAdding && (
            <button
              onClick={() => setIsAdding(true)}
              className="px-4 py-1.5 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
            >
              + 이벤트 추가
            </button>
          )}
        </div>
      </div>

      {isAdding && (
        <form onSubmit={handleSubmit} className="mb-6 p-4 bg-gray-50 dark:bg-gray-900 rounded-lg">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                이벤트 이름 *
              </label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    name: e.target.value,
                  })
                }
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="예: 기준금리 인상"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                날짜 *
              </label>
              <input
                type="date"
                value={formData.date}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    date: e.target.value,
                  })
                }
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              이벤트 유형 *
            </label>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
              {EVENT_TYPES.map((type) => (
                <button
                  key={type.value}
                  type="button"
                  onClick={() =>
                    setFormData({
                      ...formData,
                      type: type.value,
                    })
                  }
                  className={`px-3 py-2 text-sm rounded-lg border-2 transition-colors ${
                    formData.type === type.value
                      ? `border-${type.color}-500 bg-${type.color}-50 dark:bg-${type.color}-900/20 text-${type.color}-700 dark:text-${type.color}-300`
                      : 'border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500 text-gray-700 dark:text-gray-300'
                  }`}
                >
                  {type.icon} {type.label}
                </button>
              ))}
            </div>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              설명
            </label>
            <textarea
              value={formData.description}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  description: e.target.value,
                })
              }
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="이벤트에 대한 설명을 입력하세요"
              rows={3}
            />
          </div>

          <div className="flex gap-2">
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
            >
              {editingId ? '수정' : '추가'}
            </button>
            <button
              type="button"
              onClick={handleCancel}
              className="px-4 py-2 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 rounded-lg transition-colors"
            >
              취소
            </button>
          </div>
        </form>
      )}

      <div className="space-y-2">
        {events.length === 0 ? (
          <p className="text-gray-500 dark:text-gray-400 text-center py-8">
            등록된 이벤트가 없습니다
          </p>
        ) : (
          events
            .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
            .map((event) => {
              const typeConfig = getEventTypeConfig(event.type);
              return (
                <div
                  key={event.id}
                  className="flex items-start justify-between p-3 bg-gray-50 dark:bg-gray-900 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                >
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-lg">{typeConfig.icon}</span>
                      <span className="font-medium text-gray-900 dark:text-white">
                        {event.name}
                      </span>
                      <span
                        className={`px-2 py-0.5 text-xs rounded-full bg-${typeConfig.color}-100 dark:bg-${typeConfig.color}-900/30 text-${typeConfig.color}-700 dark:text-${typeConfig.color}-300`}
                      >
                        {typeConfig.label}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                      {new Date(event.date).toLocaleDateString('ko-KR', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                      })}
                    </p>
                    {event.description && (
                      <p className="text-sm text-gray-500 dark:text-gray-500">
                        {event.description}
                      </p>
                    )}
                  </div>
                  <div className="flex gap-1 ml-4">
                    <button
                      onClick={() => handleEdit(event)}
                      className="px-3 py-1 text-sm text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded transition-colors"
                    >
                      수정
                    </button>
                    <button
                      onClick={() => onDelete(event.id)}
                      className="px-3 py-1 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/30 rounded transition-colors"
                    >
                      삭제
                    </button>
                  </div>
                </div>
              );
            })
        )}
      </div>
    </div>
  );
}
