<script setup lang="ts">
import { ref } from 'vue';
import { API_BASE } from '@/utils/api';
import { useRequestDebug } from '@/composables/useRequestDebug';

const novelId = ref('');
const { request } = useRequestDebug();

async function getNovelInfo() {
  if (!novelId.value) return alert('请输入小说 ID');
  const url = `${API_BASE}/novel/${novelId.value}`;
  await request('GET', url);
}

async function getNovelContent() {
  if (!novelId.value) return alert('请输入小说 ID');
  const url = `${API_BASE}/novel/${novelId.value}/content`;
  await request('GET', url);
}

function downloadNovel() {
  if (!novelId.value) return alert('请输入小说 ID');
  window.location.href = `${API_BASE}/novel/${novelId.value}/download`;
}
</script>

<template>
  <div class="block">
    <h2>📘 单篇小说</h2>
    <input v-model.trim="novelId" placeholder="Novel ID" />
    <br />
    <button @click="getNovelInfo">信息</button>
    <button @click="getNovelContent">内容</button>
    <button @click="downloadNovel">下载 TXT</button>
  </div>
</template>