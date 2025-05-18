// 核心枚举定义
export enum MenuTypeEnum {
  MENU = "Menu", // 菜单
  BUTTON = "Button", // 按钮
}

// 类型标签映射配置
export const MenuTypeConfig = {
  [MenuTypeEnum.MENU]: {
    label: "菜单",
    type: "success" as const,
    icon: "menu",
    value: 1,
  },
  [MenuTypeEnum.BUTTON]: {
    label: "按钮",
    type: "danger" as const,
    icon: "mouse",
    value: 2,
  },
} as const;
