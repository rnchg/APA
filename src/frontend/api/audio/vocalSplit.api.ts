import request, { ssePostRequset } from "@/utils/request";

const BASE_API = import.meta.env.VITE_APP_BASE_API;
const BASE_URL = "/api/v1/audio/vocalSplit";

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
  getFolder(path: string) {
    return request<any, any>({
      url: `${BASE_URL}/getFolder`,
      method: "post",
      data: { path: path },
    });
  },
  getFileGrid(folder: string, exts: string) {
    return request<any, any>({
      url: `${BASE_URL}/getFileGrid`,
      method: "post",
      data: { folder: folder, exts: exts },
    });
  },
  getFileUrl(file: string) {
    return request<any, any>({
      url: `${BASE_URL}/getFileUrl`,
      method: "post",
      data: { file: file },
    });
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
  open(path: string) {
    return request({
      url: `${BASE_URL}/open`,
      method: "post",
      data: { path: path },
    });
  },
};

export default API;
