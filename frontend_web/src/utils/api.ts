// API请求工具
import { inject } from 'vue'

const API_BASE_URL = 'http://127.0.0.1:8000'

// 定义请求调试函数类型
interface UpdateDebugFn {
  (data: {
    method: string
    url: string
    status: string
    result?: string
  }): void
}

/**
 * 发起API请求
 * @param endpoint API端点
 * @param options 请求选项
 * @returns Promise<any> 请求结果
 */
export async function apiRequest(endpoint: string, options: RequestInit = {}): Promise<any> {
  const url = `${API_BASE_URL}${endpoint}`
  const method = options.method || 'GET'
  
  // 获取请求调试函数
  const updateDebug = inject<UpdateDebugFn>('updateDebug')
  
  // 更新请求调试信息
  updateDebug?.({
    method,
    url,
    status: 'LOADING'
  })
  
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      }
    })
    
    let data: any
    try {
      data = await response.json()
    } catch (e) {
      data = { error: 'Invalid JSON response' }
    }
    
    // 更新请求调试信息
    updateDebug?.({
      method,
      url,
      status: response.ok ? 'OK' : 'ERROR',
      result: JSON.stringify(data, null, 2)
    })
    
    if (!response.ok) {
      throw new Error(data.detail || 'Request failed')
    }
    
    return data
  } catch (error: any) {
    // 更新请求调试信息
    updateDebug?.({
      method,
      url,
      status: 'ERROR',
      result: error.message
    })
    
    throw error
  }
}

/**
 * 小说相关API
 */
export const novelApi = {
  // 搜索小说
  search: (keyword: string, page: number = 1) => {
    return apiRequest(`/novel/search?keyword=${encodeURIComponent(keyword)}&page=${page}`)
  },
  
  // 获取小说信息
  getInfo: (novelId: string) => {
    return apiRequest(`/novel/${novelId}`)
  },
  
  // 获取小说内容
  getContent: (novelId: string) => {
    return apiRequest(`/novel/${novelId}/content`)
  },
  
  // 下载小说
  download: (novelId: string) => {
    // 下载需要直接导航到URL
    window.location.href = `${API_BASE_URL}/novel/${novelId}/download`
  }
}

/**
 * 小说系列相关API
 */
export const seriesApi = {
  // 获取系列信息
  getInfo: (seriesId: string) => {
    return apiRequest(`/series/${seriesId}`)
  },
  
  // 获取系列内容
  getContent: (seriesId: string) => {
    return apiRequest(`/series/${seriesId}/content`)
  },
  
  // 下载系列
  download: (seriesId: string, mode: string = 'split') => {
    // 下载需要直接导航到URL
    window.location.href = `${API_BASE_URL}/series/${seriesId}/download?mode=${mode}`
  }
}