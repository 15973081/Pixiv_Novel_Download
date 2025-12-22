<script setup lang="ts">
import { ref, provide } from 'vue'

// 定义请求调试数据的类型
interface RequestDebugData {
  method: string
  url: string
  status: string
  result: string
}

// 初始化请求调试数据
const debugData = ref<RequestDebugData>({
  method: '',
  url: '',
  status: '',
  result: ''
})

// 提供请求调试函数给其他组件使用
const updateDebug = (data: Partial<RequestDebugData>) => {
  debugData.value = { ...debugData.value, ...data }
}

provide('updateDebug', updateDebug)
</script>

<template>
  <div class="debug-container">
    <h2 class="debug-title">📡 请求调试</h2>
    <div class="debug-info">
      <div class="debug-row">
        <span class="debug-label">Method:</span>
        <span class="debug-value">{{ debugData.method }}</span>
      </div>
      <div class="debug-row">
        <span class="debug-label">URL:</span>
        <span class="debug-value url">{{ debugData.url }}</span>
      </div>
      <div class="debug-row">
        <span class="debug-label">Status:</span>
        <span 
          class="debug-value status" 
          :class="{
            'status-loading': debugData.status === 'LOADING',
            'status-ok': debugData.status === 'OK',
            'status-error': debugData.status === 'ERROR'
          }"
        >
          {{ debugData.status }}
        </span>
      </div>
    </div>
    <div class="debug-result">
      <pre>{{ debugData.result }}</pre>
    </div>
  </div>
</template>

<style scoped>
.debug-container {
  background-color: #ffffff;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.debug-title {
  margin: 0 0 1rem 0;
  font-size: 1.3rem;
  color: #343a40;
}

.debug-info {
  margin-bottom: 1rem;
}

.debug-row {
  display: flex;
  margin-bottom: 0.5rem;
  align-items: center;
}

.debug-label {
  font-weight: 600;
  width: 80px;
  color: #495057;
}

.debug-value {
  flex: 1;
  color: #212529;
  word-break: break-all;
}

.debug-value.url {
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.9rem;
  color: #007bff;
}

.debug-value.status {
  font-weight: 700;
}

.status-loading {
  color: #ffc107;
}

.status-ok {
  color: #28a745;
}

.status-error {
  color: #dc3545;
}

.debug-result {
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  padding: 1rem;
  max-height: 300px;
  overflow-y: auto;
}

.debug-result pre {
  margin: 0;
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.9rem;
  color: #495057;
  white-space: pre-wrap;
  word-break: break-all;
}
</style>