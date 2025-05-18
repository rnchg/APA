<template>
  <div :class="['navbar__right', navbarRightClass]">
    <!-- 桌面端显示 -->
    <template v-if="isDesktop">
      <!-- 搜索 -->
      <MenuSearch />

      <!-- 全屏 -->
      <!-- <Fullscreen /> -->

      <!-- 布局大小 -->
      <!-- <SizeSelect /> -->

      <!-- 语言选择 -->
      <!-- <LangSelect /> -->

      <!-- 通知下拉 -->
      <!-- <NoticeDropdown /> -->
    </template>

    <!-- 设置面板 -->
    <div v-if="defaultSettings.showSettings" @click="settingStore.settingsVisible = true">
      <div class="i-svg:setting" />
    </div>
  </div>
</template>
<script setup lang="ts">
import defaultSettings from "@/settings";
import { DeviceEnum } from "@/enums/settings/device.enum";
import { useAppStore, useSettingsStore } from "@/store";

import { SidebarColor, ThemeMode } from "@/enums/settings/theme.enum";

const appStore = useAppStore();
const settingStore = useSettingsStore();

const isDesktop = computed(() => appStore.device === DeviceEnum.DESKTOP);

// 根据主题和侧边栏配色方案选择 navbar 右侧的样式类
const navbarRightClass = computed(() => {
  // 如果暗黑主题
  if (settingStore.theme === ThemeMode.DARK) {
    return "navbar__right--white";
  }

  // 如果侧边栏是经典蓝
  if (settingStore.sidebarColorScheme === SidebarColor.CLASSIC_BLUE) {
    return "navbar__right--white";
  }
});
</script>

<style lang="scss" scoped>
.navbar__right {
  display: flex;
  align-items: center;
  justify-content: center;

  & > * {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 40px;
    height: $navbar-height;
    color: var(--el-text-color);
    text-align: center;
    cursor: pointer;

    &:hover {
      background: rgb(0 0 0 / 10%);
    }
  }
  .user-profile {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    padding: 0 13px;

    &__avatar {
      width: 32px;
      height: 32px;
      border-radius: 50%;
    }

    &__name {
      margin-left: 10px;
    }
  }
}

.layout-top .navbar__right--white > *,
.layout-mix .navbar__right--white > * {
  color: #fff;

  // 强制所有svg图标为白色（包括通知图标）
  :deep(svg) {
    color: #fff;
    fill: #fff;
  }
}

.dark .navbar__right > *:hover {
  color: #ccc;
}
</style>
