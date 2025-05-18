import request from "@/utils/request";

const BASE_URL = "/api/v1/home";

const HomeAPI = {
  getRoutes() {
    return request<any, Route[]>({
      url: `${BASE_URL}/getRoutes`,
      method: "get",
    });
  },
};

export default HomeAPI;

export interface Route {
  children: Route[];
  component?: string;
  meta?: Meta;
  name?: string;
  path?: string;
  redirect?: string;
}

export interface Meta {
  alwaysShow?: boolean;
  hidden?: boolean;
  icon?: string;
  keepAlive?: boolean;
  title?: string;
}
