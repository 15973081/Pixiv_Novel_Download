<script setup lang="ts">
import { ref } from 'vue'
import { seriesApi } from '../utils/api'

// 定义系列信息类型
interface SeriesInfo {
  id: string
  title: string
  userName: string
  description: string
  seriesNovelCount: number
  works: Array<{
    id: string
    title: string
    createDate: string
    bookmarkCount: number
    // 其他可能的字段
  }>
  // 其他可能的字段
}

// 表单数据
const seriesId = ref('')

// 系列数据
const seriesInfo = ref<SeriesInfo | null>(null)

// 状态
const isLoading = ref(false)
const error = ref('')

// 获取系列信息
async function getSeriesInfo() {
  if (!seriesId.value.trim()) {
    error.value = '请输入系列ID'
    return
  }
  
  isLoading.value = true
  error.value = ''
  
  try {
    const data = await seriesApi.getInfo(seriesId.value)
    seriesInfo.value = data
  } catch (err: any) {
    error.value = err.message
  } finally {
    isLoading.value = false
  }
}

// 下载系列
function downloadSeries(mode: string = 'split') {
  if (!seriesId.value.trim()) {
    error.value = '请输入系列ID'
    return
  }
  
  seriesApi.download(seriesId.value, mode)
}
</script>

<template>
  <div class="series-container">
    <h2 class="section-title">📚 小说系列</h2>
    
    <!-- 系列ID输入 -->
    <div class="series-id-form">
      <input 
        type="text" 
        v-model="seriesId" 
        placeholder="输入系列ID" 
        class="series-id-input"
      />
      <button 
        @click="getSeriesInfo" 
        class="info-button"
        :disabled="isLoading"
      >
        {{ isLoading ? '获取中...' : '获取信息' }}
      </button>
    </div>
    
    <!-- 错误信息 -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    
    <!-- 系列信息 -->
    <div v-if="seriesInfo" class="series-info-section">
      <div class="series-header">
        <h3 class="series-title">{{ seriesInfo.title }}</h3>
        <p class="series-author">作者: {{ seriesInfo.userName }}</p>
        <p class="series-count">包含 {{ seriesInfo.seriesNovelCount }} 篇小说</p>
      </div>
      
      <div class="series-description">
        <h4>系列简介</h4>
        <p>{{ seriesInfo.description }}</p>
      </div>
      
      <div class="series-actions">
        <button 
          @click="downloadSeries('split')" 
          class="download-button"
        >
          📥 分章下载
        </button>
        <button 
          @click="downloadSeries('merge')" 
          class="download-button merge-button"
        >
          📥 合并下载
        </button>
      </div>
      
      <div class="series-novels">
        <h4>系列小说列表</h4>
        <div class="novel-list">
          <div 
            v-for="novel in seriesInfo.works" 
            :key="novel.id" 
            class="novel-item"
          >
            <div class="novel-info">
              <h5 class="novel-title">{{ novel.title }}</h5>
              <div class="novel-meta">
                <span class="novel-date">发布于: {{ novel.createDate }}</span>
                <span class="novel-bookmarks">❤ {{ novel.bookmarkCount || 0 }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 未获取信息 -->
    <div v-else-if="!isLoading && !error" class="no-info">
      <p>请输入系列ID并点击获取信息</p>
    </div>
  </div>
</template>

<style scoped>
.series-container {
  width: 100%;
}

.section-title {
  margin: 0 0 1.5rem 0;
  font-size: 1.4rem;
  color: #343a40;
}

.series-id-form {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.series-id-input {
  flex: 1;
  min-width: 200px;
  padding: 0.75rem;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s ease;
}

.series-id-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.25);
}

.info-button {
  padding: 0.75rem 1.5rem;
  background-color: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.info-button:hover {
  background-color: #5a67d8;
}

.info-button:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
}

.error-message {
  color: #dc3545;
  background-color: #f8d7da;
  padding: 0.75rem;
  border-radius: 6px;
  margin-bottom: 1.5rem;
}

.series-info-section {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.series-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #e9ecef;
}

.series-title {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  color: #212529;
}

.series-author {
  margin: 0 0 0.5rem 0;
  color: #6c757d;
  font-size: 1rem;
}

.series-count {
  margin: 0;
  color: #9fa8da;
  font-size: 0.9rem;
}

.series-description {
  margin-bottom: 1.5rem;
}

.series-description h4 {
  margin: 0 0 0.5rem 0;
  color: #343a40;
  font-size: 1.1rem;
}

.series-description p {
  margin: 0;
  color: #6c757d;
  line-height: 1.6;
}

.series-actions {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.download-button {
  padding: 0.75rem 1.5rem;
  background-color: #ed8936;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.download-button:hover {
  background-color: #dd6b20;
}

.merge-button {
  background-color: #48bb78;
}

.merge-button:hover {
  background-color: #38a169;
}

.series-novels h4 {
  margin: 0 0 1rem 0;
  color: #343a40;
  font-size: 1.1rem;
}

.novel-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.novel-item {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 6px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.novel-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.novel-info h5 {
  margin: 0 0 0.5rem 0;
  color: #212529;
  font-size: 1.1rem;
}

.novel-meta {
  display: flex;
  gap: 1.5rem;
  color: #6c757d;
  font-size: 0.9rem;
}

.no-info {
  text-align: center;
  color: #6c757d;
  padding: 2rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .series-id-form {
    flex-direction: column;
  }
  
  .series-id-input {
    width: 100%;
  }
  
  .series-actions {
    flex-direction: column;
  }
  
  .novel-meta {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>