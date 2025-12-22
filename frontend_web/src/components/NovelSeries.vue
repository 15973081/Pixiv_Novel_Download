<script setup lang="ts">
import { ref } from 'vue';
import { API_BASE } from '@/utils/api';
import { useRequestDebug } from '@/composables/useRequestDebug';

const seriesId = ref('');
const mode = ref<'split' | 'merge'>('split');
const { request } = useRequestDebug();

async function getSeriesInfo() {
  if (!seriesId.value) return alert('请输入系列 ID');
  const url = `${API_BASE}/series/${seriesId.value}`;
  await request('GET', url);
}

async function getSeriesContent() {
  if (!seriesId.value) return alert('请输入系列 ID');
  const url = `${API_BASE}/series/${seriesId.value}/content`;
  await request('GET', url);
}

function downloadSeries() {
  if (!seriesId.value) return alert('请输入系列 ID');
  window.location.href = `${API_BASE}/series/${seriesId.value}/download?mode=${mode}`;
}
</script>

<template>
  <div class="block">
    <h2>📚 小说系列</h2>
    <input v-model.trim="seriesId" placeholder="Series ID" />
    <br />
    <button @click="getSeriesInfo">系列信息</button>
    <button @click="getSeriesContent">章节 ID</button>
    <br /><br />
    <select v-model="mode">
      <option value="split">split（zip）</option>
      <option value="merge">merge（txt）</option>
    </select>
    <button @click="downloadSeries">下载系列</button>
  </div>
</template>