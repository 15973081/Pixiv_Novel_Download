// src/composables/useRequestDebug.ts
import { inject } from 'vue';
import { API_BASE } from '../utils/api';

type DebugExpose = {
    updateRequest: (raw: string) => void;
    updateSuccess: (raw: string) => void;
    updateError: (raw: string) => void;
};

export function useRequestDebug() {
    // ⚠️ inject 到的是 Ref，而不是直接的实例
    const requestDebugRef = inject<{ value: DebugExpose | null }>(
        'requestDebug',
        { value: null }
    );

    function getDebug() {
        return requestDebugRef?.value ?? null;
    }

    async function request(method: string, fullUrl: string) {
        const url = fullUrl.startsWith('http')
            ? fullUrl
            : `${API_BASE}${fullUrl}`;

        // 请求开始（统一 string）
        getDebug()?.updateRequest(
            JSON.stringify({ method, url }, null, 2)
        );

        try {
            const res = await fetch(url);
            const contentType = res.headers.get('content-type') || '';

            let raw: string;

            if (contentType.includes('application/json')) {
                raw = JSON.stringify(await res.json(), null, 2);
            } else {
                raw = JSON.stringify(
                    { message: '非 JSON 响应（可能是下载或流）' },
                    null,
                    2
                );
            }

            if (res.ok) {
                getDebug()?.updateSuccess(raw);
            } else {
                getDebug()?.updateError(raw);
            }

            return raw;

        } catch (e: any) {
            const err = JSON.stringify(
                { error: e?.toString?.() ?? '未知错误' },
                null,
                2
            );
            getDebug()?.updateError(err);
            throw e;
        }
    }

    return { request };
}
