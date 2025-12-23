<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRequestDebug } from '@/composables/useRequestDebug';

/**
 * Debug 组件 ref
 * Debug.result === 原始 JSON 字符串
 */
const requestDebug = ref<any | null>(null);
const { request } = useRequestDebug();

/**
 * 结果状态
 */
type ResultType =
    | 'search'
    | 'novel'
    | 'content'
    | 'series'
    | 'seriesContent'
    | 'error'
    | null;

const resultType = ref<ResultType>(null);
const resultData = ref<any>(null);
const errorMsg = ref('');

/**
 * 展示层兜底工具（不是接口定义）
 */
function getAuthor(data: any): string {
  return data?.author || data?.userName || data?.userId || '未知作者';
}

function getTitle(data: any): string {
  return data?.title || '无标题';
}

function getDescription(data: any): string {
  return data?.description || data?.caption || '';
}

function formatDate(d?: string) {
  return d ? new Date(d).toLocaleString() : '未知';
}

/**
 * 核心：根据【接口文档】判断返回类型
 */
watch(
    () => requestDebug.value?.result,
    (raw) => {
      resultType.value = null;
      resultData.value = null;
      errorMsg.value = '';

      if (!raw || typeof raw !== 'string') return;

      try {
        const data = JSON.parse(raw);

        if (typeof data !== 'object' || data === null) {
          throw new Error('非对象 JSON');
        }

        /**
         * ⚠️ 判断顺序非常重要（严格按接口文档）
         */

        // /novel/search
        if (data.novel && Array.isArray(data.novel.data)) {
          resultType.value = 'search';
          resultData.value = data.novel;
          return;
        }

        // /novel/{id}/content
        if (typeof data.content === 'string') {
          resultType.value = 'content';
          resultData.value = data;
          return;
        }

        // /series/series/{id}/content
        if (Array.isArray(data.novel_ids)) {
          resultType.value = 'seriesContent';
          resultData.value = data;
          return;
        }

        // /series/series/{id}
        if ('displaySeriesContentCount' in data) {
          resultType.value = 'series';
          resultData.value = data;
          return;
        }

        // /novel/{id}
        if ('pageCount' in data && data.id && data.title) {
          resultType.value = 'novel';
          resultData.value = data;
          return;
        }

        // 兜底
        resultType.value = 'error';
        errorMsg.value = '无法识别的接口返回结构';

      } catch (e) {
        resultType.value = 'error';
        errorMsg.value = 'JSON 解析失败或非 JSON 响应';
      }
    },
    { immediate: true }
);
</script>

<template>
  <div class="page">
    <!-- 示例请求按钮 -->
    <button @click="request('GET', '/novel/search?keyword=原神&page=1')">
      测试请求
    </button>

    <!-- Debug 区（必须 expose result） -->
    <RequestDebug ref="requestDebug" />

    <!-- ================== -->
    <!-- 解析展示区 -->
    <!-- ================== -->
    <div v-if="resultType" class="result-display">
      <h2>📤 接口返回解析结果</h2>

      <!-- 搜索结果 -->
      <div v-if="resultType === 'search'">
        <div
            v-for="item in resultData.data"
            :key="item.id"
            class="novel-card"
        >
          <img
              :src="item.url || 'https://via.placeholder.com/120x160'"
              class="cover"
          />
          <div class="info">
            <h3>{{ getTitle(item) }}</h3>
            <p class="author">作者：{{ getAuthor(item) }}</p>
            <p v-if="getDescription(item)" v-html="getDescription(item)" />
            <p class="meta">
              字数：{{ item.wordCount ?? '未知' }} |
              创建：{{ formatDate(item.createDate) }}
            </p>
          </div>
        </div>
      </div>

      <!-- 单篇小说信息 -->
      <div v-else-if="resultType === 'novel'">
        <h3>{{ getTitle(resultData) }}</h3>
        <p>作者：{{ getAuthor(resultData) }}</p>
        <p v-html="getDescription(resultData)" />
      </div>

      <!-- 小说正文 -->
      <div v-else-if="resultType === 'content'">
        <h3>{{ getTitle(resultData) }}</h3>
        <p class="author">作者：{{ getAuthor(resultData) }}</p>
        <div
            class="content"
            v-html="resultData.content.replace(/\n/g, '<br>')"
        />
      </div>

      <!-- 系列信息 -->
      <div v-else-if="resultType === 'series'">
        <h3>{{ getTitle(resultData) }}</h3>
        <p>作者：{{ getAuthor(resultData) }}</p>
        <p v-html="getDescription(resultData)" />
        <img
            v-if="resultData.cover"
            :src="resultData.cover"
            class="series-cover"
        />
      </div>

      <!-- 系列章节 -->
      <div v-else-if="resultType === 'seriesContent'">
        <h3>系列章节 ID</h3>
        <div class="chapter-list">
          <span
              v-for="id in resultData.novel_ids"
              :key="id"
              class="chapter-id"
          >
            {{ id }}
          </span>
        </div>
      </div>

      <!-- 错误 -->
      <div v-else-if="resultType === 'error'" class="error">
        ⚠️ {{ errorMsg }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.page {
  padding: 2rem;
}

.result-display {
  margin-top: 2rem;
  background: #fff;
  padding: 1.5rem;
  border-radius: 12px;
}

.novel-card {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.cover {
  width: 120px;
  height: 160px;
  object-fit: cover;
}

.author {
  color: #667eea;
}

.content {
  line-height: 1.9;
}

.series-cover {
  max-width: 400px;
  margin-top: 1rem;
}

.chapter-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.chapter-id {
  background: #667eea;
  color: #fff;
  padding: 6px 12px;
  border-radius: 20px;
}

.error {
  color: #d32f2f;
}
</style>
