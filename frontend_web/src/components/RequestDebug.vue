<script setup lang="ts">
import { ref } from 'vue';

const method = ref('');
const url = ref('');
const status = ref('');
const result = ref('');

function updateRequest(info: { method: string; url: string }) {
  method.value = info.method;
  url.value = info.url;
  status.value = 'LOADING';
  result.value = '';
}

function updateSuccess(data: any) {
  status.value = 'OK';
  result.value = JSON.stringify(data, null, 2);
}

function updateError(error: any) {
  status.value = 'ERROR';
  result.value = typeof error === 'string' ? error : error.detail || JSON.stringify(error, null, 2);
}

defineExpose({ updateRequest, updateSuccess, updateError });
</script>

<template>
  <div class="block">
    <h2>📡 请求调试</h2>
    <div>Method: <span>{{ method }}</span></div>
    <div>URL: <span>{{ url }}</span></div>
    <div>Status: <span :class="['status', { ok: status === 'OK', err: status === 'ERROR' }]">{{ status }}</span></div>
    <pre>{{ result }}</pre>
  </div>
</template>

<style scoped>
pre {
  background: #f6f6f6;
  padding: 10px;
  max-height: 300px;
  overflow: auto;
  white-space: pre-wrap;
}
.status { font-weight: bold; }
.ok { color: green; }
.err { color: red; }
</style>