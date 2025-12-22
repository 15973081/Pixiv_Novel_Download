// src/composables/useRequestDebug.ts
import { getCurrentInstance } from 'vue';
import {API_BASE} from "../utils/api";


export function useRequestDebug() {
    const instance = getCurrentInstance();
    const debug = instance?.proxy?.$refs.requestDebug as any;

    async function request(method: string, fullUrl: string) {
        const url = fullUrl.startsWith('http') ? fullUrl : `${API_BASE}${fullUrl}`;
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
    }

    return { request };
}