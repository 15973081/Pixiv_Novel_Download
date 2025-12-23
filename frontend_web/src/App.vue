<script setup lang="ts">
import { ref, provide } from 'vue';
import RequestDebug from '@/components/RequestDebug.vue';
import NovelSearch from '@/components/NovelSearch.vue';
import NovelDetail from '@/components/NovelDetail.vue';
import NovelSeries from '@/components/NovelSeries.vue';

// 创建RequestDebug组件的引用
const requestDebug = ref();

// 提供RequestDebug组件实例给子组件
provide('requestDebug', requestDebug);
</script>

<template>
  <div class="app-container">
    <!-- 头部 -->
    <header class="app-header">
      <h1 class="app-title">📖 Pixiv Novel Downloader</h1>
      <p class="app-subtitle">原型前端（Vue 版）– 可调试</p>
    </header>

    <!-- 主要内容区 -->
    <main class="app-main">
      <!-- 请求调试区 -->
      <RequestDebug ref="requestDebug" />

      <!-- 功能区块 -->
      <section class="block">
        <NovelSearch />
      </section>

      <section class="block">
        <NovelDetail />
      </section>

      <section class="block">
        <NovelSeries />
      </section>
    </main>

    <!-- 底部 -->
    <footer class="app-footer">
      Powered by Vue 3 + Vite • API: http://127.0.0.1:8000
    </footer>
  </div>
</template>

<style scoped>
/* 整体容器 */
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f0f2f5;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* 渐变头部 */
.app-header {
  padding: 3rem 2rem;
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px 12px 0 0;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
}

.app-title {
  margin: 0;
  font-size: 2.8rem;
  font-weight: 800;
  letter-spacing: -0.5px;
}

.app-subtitle {
  margin: 0.8rem 0 0;
  font-size: 1.2rem;
  opacity: 0.95;
  font-weight: 400;
}

/* 主内容区 */
.app-main {
  flex: 1;
  padding: 2rem;
  max-width: 1000px;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
}

/* 每个功能区块（卡片样式） */
.block {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  border: 1px solid #e9ecef;
  transition: transform 0.2s, box-shadow 0.2s;
}

.block:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
}

.block h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #333;
  font-size: 1.5rem;
  border-bottom: 2px solid #667eea;
  padding-bottom: 0.5rem;
  display: inline-block;
}

/* 输入框和按钮美化 */
input, select, button {
  padding: 10px 14px;
  margin: 6px 8px 6px 0;
  font-size: 15px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  transition: all 0.2s;
}

input:focus, select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
}

button {
  cursor: pointer;
  background: #667eea;
  color: white;
  border: none;
  font-weight: 600;
  min-width: 100px;
}

button:hover {
  background: #5a6fd8;
  transform: translateY(-1px);
}

button:active {
  transform: translateY(0);
}

/* 底部 */
.app-footer {
  padding: 1.5rem;
  text-align: center;
  color: #6c757d;
  font-size: 0.95rem;
  background: #ffffff;
  border-top: 1px solid #e9ecef;
  margin-top: auto;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .app-header {
    padding: 2rem 1.5rem;
  }

  .app-title {
    font-size: 2.2rem;
  }

  .app-main {
    padding: 1rem;
  }

  .block {
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }

  input, select, button {
    width: 100%;
    margin: 8px 0;
  }

  button {
    min-width: auto;
  }
}
</style>