import axios, { type InternalAxiosRequestConfig, type AxiosResponse } from "axios";
import qs from "qs";
import { ResultEnum } from "@/enums/api/result.enum";
import { fetchEventSource } from "@microsoft/fetch-event-source";

// 创建 axios 实例
const service = axios.create({
  baseURL: import.meta.env.VITE_APP_BASE_API,
  timeout: 50000,
  headers: { "Content-Type": "application/json;charset=utf-8" },
  paramsSerializer: (params) => qs.stringify(params),
});
// 请求拦截器
service.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    return config;
  },
  (error) => Promise.reject(error)
);
// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse) => {
    // 如果响应是二进制流，则直接返回，用于下载文件、Excel 导出等
    if (response.config.responseType === "blob") {
      return response;
    }
    const { success, code, message, data } = response.data;
    if (code === ResultEnum.OK) {
      return data;
    }
    ElMessage.error(message || "系统出错");
    return Promise.reject(new Error(message || "Error"));
  },
  async (error) => {
    const { config, response } = error;
    if (response) {
      const { success, code, message, data } = response.data;
      if (code === ResultEnum.UNAUTHORIZED || code === ResultEnum.FORBIDDEN) {
        return Promise.reject(new Error(message || "Error"));
      } else {
        ElMessage.error(message || "系统出错");
      }
    }
    return Promise.reject(error.message);
  }
);
export default service;

export function sseGetRequset(
  url: string,
  onmessage: ((this: EventSource, ev: MessageEvent) => any) | null,
  onerror: ((this: EventSource, ev: Event) => any) | null = null,
  onopen: ((this: EventSource, ev: Event) => any) | null = null
) {
  const sse = new EventSource(url);
  sse.onmessage = onmessage;
  sse.onerror = onerror;
  sse.onopen = onopen;
}

export function ssePostRequset(
  url: string,
  obj: object,
  onmessage: (ev: EventSourceMessage, ac: AbortController) => void,
  onerror: (err: any, ac: AbortController) => number | null | undefined | void
) {
  const ac = new AbortController();
  fetchEventSource(url, {
    method: "POST",
    signal: ac.signal,
    headers: {
      "Content-Type": "application/json",
      Accept: "*/*",
    },
    openWhenHidden: true,
    body: JSON.stringify(obj),
    onmessage(msg) {
      onmessage(msg, ac);
    },
    onerror(err) {
      onerror(err, ac);
      throw err;
    },
  });
}
