<script setup lang="ts">
import { ref } from 'vue'
import { novelApi } from '../utils/api'

// 定义小说搜索结果的类型
interface NovelSearchResult {
  id: string
  title: string
  userName: string
  createDate: string
  bookmarkCount: number
  commentCount: number
  likeCount: number
  // 其他可能的字段
}

// 表单数据
const keyword = ref('')
const page = ref(1)

// 搜索结果
const searchResults = ref<NovelSearchResult[]>([])
const totalResults = ref(0)
const isLoading = ref(false)
const error = ref('')

// 搜索小说
async function searchNovel() {
  if (!keyword.value.trim()) {
    error.value = '请输入搜索关键词'
    return
  }
  
  isLoading.value = true
  error.value = ''
  
  try {
    const results = await novelApi.search(keyword.value, page.value)
    
    // 根据API返回的实际结构调整
    searchResults.value = results.works || []
    totalResults.value = results.total || 0
  } catch (err: any) {
    error.value = err.message
  } finally {
    isLoading.value = false
  }
}

// 上一页
function previousPage() {
  if (page.value > 1) {
    page.value--
    searchNovel()
  }
}

// 下一页
function nextPage() {
  if (searchResults.value.length > 0) {
    page.value++
    searchNovel()
  }
}
</script>

<template>
  <div class="search-container">
    <h2 class="section-title">🔍 搜索小说</h2>
    
    <!-- 搜索表单 -->
    <div class="search-form">
      <input 
        type="text" 
        v-model="keyword" 
        placeholder="输入关键词" 
        class="search-input"
      />
      <input 
        type="number" 
        v-model="page" 
        min="1" 
        class="page-input"
      />
      <button 
        @click="searchNovel" 
        class="search-button"
        :disabled="isLoading"
      >
        {{ isLoading ? '搜索中...' : '搜索' }}
      </button>
    </div>
    
    <!-- 错误信息 -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    
    <!-- 搜索结果 -->
    <div v-if="searchResults.length > 0" class="results-container">
      <div class="results-info">
        <p>共找到 {{ totalResults }} 个结果</p>
      </div>
      
      <div class="novel-list">
        <div 
          v-for="novel in searchResults" 
          :key="novel.id" 
          class="novel-item"
        >
          <div class="novel-info">
            <h3 class="novel-title">{{ novel.title }}</h3>
            <p class="novel-author">作者: {{ novel.userName }}</p>
            <div class="novel-stats">
              <span class="stat-item">❤ {{ novel.bookmarkCount || 0 }}</span>
              <span class="stat-item">💬 {{ novel.commentCount || 0 }}</span>
              <span class="stat-item">⭐ {{ novel.likeCount || 0 }}</span>
            </div>
            <p class="novel-date">发布于: {{ novel.createDate }}</p>
          </div>
        </div>
      </div>
      
      <!-- 分页 -->
      <div class="pagination">
        <button 
          @click="previousPage" 
          :disabled="page <= 1"
          class="page-button"
        >
          上一页
        </button>
        <span class="page-number">第 {{ page }} 页</span>
        <button 
          @click="nextPage" 
          :disabled="!searchResults.length"
          class="page-button"
        >
          下一页
        </button>
      </div>
    </div>
    
    <!-- 无结果 -->
    <div v-else-if="!isLoading && !error" class="no-results">
      <p>暂无搜索结果</p>
    </div>
  </div>
</template>

<style scoped>
.search-container {
  width: 100%;
}

.section-title {
  margin: 0 0 1.5rem 0;
  font-size: 1.4rem;
  color: #343a40;
}

.search-form {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.search-input {
  flex: 1;
  min-width: 200px;
  padding: 0.75rem;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.25);
}

.page-input {
  width: 80px;
  padding: 0.75rem;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  font-size: 1rem;
  text-align: center;
}

.search-button {
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

.search-button:hover {
  background-color: #5a67d8;
}

.search-button:disabled {
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

.results-container {
  margin-top: 1.5rem;
}

.results-info {
  margin-bottom: 1rem;
  color: #6c757d;
  font-size: 0.9rem;
}

.novel-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.novel-item {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.novel-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.novel-title {
  margin: 0 0 0.5rem 0;
  font-size: 1.2rem;
  color: #212529;
}

.novel-author {
  margin: 0 0 0.75rem 0;
  color: #6c757d;
  font-size: 0.9rem;
}

.novel-stats {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.stat-item {
  color: #6c757d;
  font-size: 0.9rem;
}

.novel-date {
  margin: 0;
  color: #9fa8da;
  font-size: 0.85rem;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
}

.page-button {
  padding: 0.5rem 1rem;
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  color: #495057;
  cursor: pointer;
  transition: all 0.2s ease;
}

.page-button:hover:not(:disabled) {
  background-color: #e9ecef;
}

.page-button:disabled {
  color: #adb5bd;
  cursor: not-allowed;
}

.page-number {
  color: #495057;
  font-weight: 500;
}

.no-results {
  text-align: center;
  color: #6c757d;
  padding: 2rem;
  background-color: white;
  border-radius: 8px;
}
</style>