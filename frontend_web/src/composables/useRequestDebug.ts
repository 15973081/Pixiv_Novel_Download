// src/composables/useRequestDebug.ts
import { inject } from 'vue';
import {API_BASE} from "../utils/api";

export function useRequestDebug() {
    // 从App.vue中获取提供的RequestDebug组件实例
    const requestDebug = inject<{ value: any }>('requestDebug');
    const debug = requestDebug?.value;

    async function request(method: string, fullUrl: string) {
        const url = fullUrl.startsWith('http') ? fullUrl : `${API_BASE}${fullUrl}`;
        
        // 确保debug存在再调用方法
        if (debug) {
            debug.updateRequest({ method, url });

            try {
                const res = await fetch(url);
                const data = await res.json();

                if (res.ok) {
                    debug.updateSuccess(data);
                } else {
                    debug.updateError(data);
                }
                return data;
            } catch (e: any) {
                debug.updateError(e.toString());
                throw e;
            }
        } else {
            // 如果debug不存在，仍然执行请求但不更新调试信息
            try {
                const res = await fetch(url);
                return res.json();
            } catch (e) {
                throw e;
            }
        }
    }

    return { request };
}