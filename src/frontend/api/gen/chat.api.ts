import request, { ssePostRequset } from "@/utils/request";

const BASE_API = import.meta.env.VITE_APP_BASE_API;
const BASE_URL = "/api/v1/gen/chat";

const API = {
  getConfig() {
    return request<any, any>({
      url: `${BASE_URL}/getConfig`,
      method: "post",
    });
  },
  setConfig(data: any) {
    return request<any, any>({
      url: `${BASE_URL}/setConfig`,
      method: "post",
      data: { data: data },
    });
  },
  getInit() {
    return request<any, any>({
      url: `${BASE_URL}/getInit`,
      method: "post",
    });
  },
  init(data: object, onmessage: any, onerror: any) {
    return ssePostRequset(`${BASE_API}${BASE_URL}/init`, { data: data }, onmessage, onerror);
  },
  start(data: object, onmessage: any, onerror: any) {
    return ssePostRequset(`${BASE_API}${BASE_URL}/start`, { data: data }, onmessage, onerror);
  },
  stop() {
    return request({
      url: `${BASE_URL}/stop`,
      method: "post",
    });
  },
};

export default API;
