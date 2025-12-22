<script setup lang="ts">
import { ref, reactive } from 'vue'
import { novelApi } from '../utils/api'

// 定义小说详情类型
interface NovelInfo {
  id: string
  title: string
  userName: string
  createDate: string
  uploadDate: string
  bookmarkCount: number
  commentCount: number
  likeCount: number
  description: string
  // 其他可能的字段
}

// 定义小说内容类型
interface NovelContent {
  content: string
  // 其他可能的字段
}

// 表单数据
const novelId = ref('')

// 小说数据
const novelInfo = ref<NovelInfo | null>(null)
const novelContent = ref<NovelContent | null>(null)

// 状态
const isLoading = ref(false)
const isLoadingContent = ref(false)
const error = ref('')
const errorContent = ref('')

// 获取小说信息
async function getNovelInfo() {
  if (!novelId.value.trim()) {
    error.value = '请输入小说ID'
    return
  }
  
  isLoading.value = true
  error.value = ''
  
  try {
    const data = await novelApi.getInfo(novelId.value)
    novelInfo.value = data
    novelContent.value = null // 清除内容，让用户可以重新加载
  } catch (err: any) {
    error.value = err.message
  } finally {
    isLoading.value = false
  }
}

// 获取小说内容
async function getNovelContent() {
  if (!novelId.value.trim()) {
    errorContent.value = '请先获取小说信息'
    return
  }
  
  isLoadingContent.value = true
  errorContent.value = ''
  
  try {
    const data = await novelApi.getContent(novelId.value)
    novelContent.value = data
  } catch (err: any) {
    errorContent.value = err.message
  } finally {
    isLoadingContent.value = false
  }
}

// 下载小说
function downloadNovel() {
  if (!novelId.value.trim()) {
    error.value = '请输入小说ID'
    return
  }
  
  novelApi.download(novelId.value)
}
</script>

<template>
  <div class="novel-detail-container">
    <h2 class="section-title">📘 单篇小说</h2>
    
    <!-- 小说ID输入 -->
    <div class="novel-id-form">
      <input 
        type="text" 
        v-model="novelId" 
        placeholder="输入小说ID" 
        class="novel-id-input"
      />
      <button 
        @click="getNovelInfo" 
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
    
    <!-- 小说信息 -->
    <div v-if="novelInfo" class="novel-info-section">
      <div class="novel-header">
        <h3 class="novel-title">{{ novelInfo.title }}</h3>
        <p class="novel-author">作者: {{ novelInfo.userName }}</p>
      </div>
      
      <div class="novel-meta">
        <div class="novel-stats">
          <span class="stat-item">❤ {{ novelInfo.bookmarkCount || 0 }}</span>
          <span class="stat-item">💬 {{ novelInfo.commentCount || 0 }}</span>
          <span class="stat-item">⭐ {{ novelInfo.likeCount || 0 }}</span>
        </div>
        <div class="novel-dates">
          <span class="date-item">创建于: {{ novelInfo.createDate }}</span>
          <span class="date-item">更新于: {{ novelInfo.uploadDate }}</span>
        </div>
      </div>
      
      <div class="novel-description">
        <h4>简介</h4>
        <p>{{ novelInfo.description }}</p>
      </div>
      
      <div class="novel-actions">
        <button 
          @click="getNovelContent" 
          class="content-button"
          :disabled="isLoadingContent"
        >
          {{ isLoadingContent ? '加载中...' : '加载内容' }}
        </button>
        <button 
          @click="downloadNovel" 
          class="download-button"
        >
          📥 下载小说
        </button>
      </div>
    </div>
    
    <!-- 小说内容 -->
    <div v-if="novelContent" class="novel-content-section">
      <h4 class="content-title">小说内容</h4>
      <div v-if="errorContent" class="error-message">
        {{ errorContent }}
      </div>
      <div class="novel-content">
        <!-- 使用 v-html 显示带有格式的内容 -->
        <div v-html="novelContent.content"></div>
      </div>
    </div>
    
    <!-- 未获取信息 -->
    <div v-else-if="!isLoading && !error" class="no-info">
      <p>请输入小说ID并点击获取信息</p>
    </div>
  </div>
</template>

<style scoped>
.novel-detail-container {
  width: 100%;
}

.section-title {
  margin: 0 0 1.5rem 0;
  font-size: 1.4rem;
  color: #343a40;
}

.novel-id-form {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.novel-id-input {
  flex: 1;
  min-width: 200px;
  padding: 0.75rem;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s ease;
}

.novel-id-input:focus {
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

.novel-info-section {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
}

.novel-header {
  margin-bottom: 1.5rem;
}

.novel-title {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  color: #212529;
}

.novel-author {
  margin: 0;
  color: #6c757d;
  font-size: 1rem;
}

.novel-meta {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #e9ecef;
}

.novel-stats {
  display: flex;
  gap: 1.5rem;
}

.stat-item {
  color: #6c757d;
  font-size: 1rem;
  font-weight: 500;
}

.novel-dates {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.date-item {
  color: #9fa8da;
  font-size: 0.9rem;
}

.novel-description {
  margin-bottom: 1.5rem;
}

.novel-description h4 {
  margin: 0 0 0.5rem 0;
  color: #343a40;
  font-size: 1.1rem;
}

.novel-description p {
  margin: 0;
  color: #6c757d;
  line-height: 1.6;
}

.novel-actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.content-button {
  padding: 0.75rem 1.5rem;
  background-color: #48bb78;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.content-button:hover {
  background-color: #38a169;
}

.content-button:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
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

.novel-content-section {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.content-title {
  margin: 0 0 1rem 0;
  color: #343a40;
  font-size: 1.1rem;
}

.novel-content {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 6px;
  min-height: 200px;
  line-height: 1.7;
  white-space: pre-wrap;
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
  .novel-id-form {
    flex-direction: column;
  }
  
  .novel-id-input {
    width: 100%;
  }
  
  .novel-stats {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .novel-dates {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .novel-actions {
    flex-direction: column;
  }
}
</style>