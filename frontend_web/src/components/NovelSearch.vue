<script setup lang="ts">
import { ref } from 'vue';
import { API_BASE } from '@/utils/api';
import {useRequestDebug} from "@/composables/useRequestDebug";

const keyword = ref('');
const page = ref(1);

const { request } = useRequestDebug();

async function searchNovel() {
  if (!keyword.value.trim()) return;
  const url = `${API_BASE}/novel/search?keyword=${encodeURIComponent(keyword.value)}&page=${page.value}`;
  await request('GET', url);
}
</script>

<template>
  <div class="block">
    <h2>🔍 搜索小说</h2>
    <input v-model="keyword" placeholder="关键词" />
    <input v-model.number="page" type="number" min="1" />
    <button @click="searchNovel">搜索</button>
  </div>
</template>