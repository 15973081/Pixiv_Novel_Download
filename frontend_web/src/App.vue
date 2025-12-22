<script setup lang="ts">
import { ref } from 'vue'
import RequestDebug from './components/RequestDebug.vue'
import NovelSearch from './components/NovelSearch.vue'
import NovelDetail from './components/NovelDetail.vue'
import NovelSeries from './components/NovelSeries.vue'

const activeSection = ref('search')
</script>

<template>
  <div class="app-container">
    <!-- 头部 -->
    <header class="app-header">
      <h1 class="app-title">📖 Pixiv Novel Downloader</h1>
      <p class="app-subtitle">方便快捷地下载Pixiv小说</p>
    </header>

    <!-- 导航 -->
    <nav class="app-nav">
      <button 
        class="nav-button" 
        :class="{ active: activeSection === 'search' }"
        @click="activeSection = 'search'"
      >
        🔍 搜索小说
      </button>
      <button 
        class="nav-button" 
        :class="{ active: activeSection === 'novel' }"
        @click="activeSection = 'novel'"
      >
        📘 单篇小说
      </button>
      <button 
        class="nav-button" 
        :class="{ active: activeSection === 'series' }"
        @click="activeSection = 'series'"
      >
        📚 小说系列
      </button>
    </nav>

    <!-- 主要内容 -->
    <main class="app-main">
      <!-- 请求调试区 -->
      <RequestDebug />

      <!-- 内容区域 -->
      <div class="content-section">
        <section v-if="activeSection === 'search'" class="section-content">
          <NovelSearch />
        </section>
        <section v-else-if="activeSection === 'novel'" class="section-content">
          <NovelDetail />
        </section>
        <section v-else-if="activeSection === 'series'" class="section-content">
          <NovelSeries />
        </section>
      </div>
    </main>

    <!-- 页脚 -->
    <footer class="app-footer">
      <p>&copy; 2025 Pixiv Novel Downloader | Made with Vue 3</p>
    </footer>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin: 20px;
}

.app-header {
  padding: 2rem;
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 8px 8px 0 0;
}

.app-title {
  margin: 0;
  font-size: 2.5rem;
  font-weight: 700;
}

.app-subtitle {
  margin: 0.5rem 0 0 0;
  font-size: 1.1rem;
  opacity: 0.9;
}

.app-nav {
  display: flex;
  background-color: #f8f9fa;
  padding: 0.5rem;
  border-bottom: 1px solid #e9ecef;
}

.nav-button {
  flex: 1;
  padding: 1rem;
  margin: 0 0.25rem;
  border: none;
  background-color: transparent;
  color: #495057;
  font-size: 1rem;
  font-weight: 500;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.nav-button:hover {
  background-color: #e9ecef;
  color: #212529;
}

.nav-button.active {
  background-color: #667eea;
  color: white;
}

.app-main {
  flex: 1;
  padding: 2rem;
}

.content-section {
  margin-top: 2rem;
}

.section-content {
  background-color: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.app-footer {
  padding: 1rem;
  text-align: center;
  color: #6c757d;
  border-top: 1px solid #e9ecef;
  font-size: 0.9rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .app-container {
    margin: 0;
    border-radius: 0;
  }
  
  .app-header {
    padding: 1.5rem;
  }
  
  .app-title {
    font-size: 2rem;
  }
  
  .app-nav {
    flex-direction: column;
  }
  
  .nav-button {
    margin: 0.25rem 0;
  }
  
  .app-main {
    padding: 1rem;
  }
  
  .section-content {
    padding: 1.5rem;
  }
}
</style>
