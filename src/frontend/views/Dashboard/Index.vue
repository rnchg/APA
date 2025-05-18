<template>
  <div class="app-container">
    <el-card class="mb-2">
      <el-row :gutter="10">
        <el-image :src="dashboard" fit="cover" style="width: 100%; height: 220px" />
      </el-row>
    </el-card>
    <el-card class="mb-2">
      <el-row :gutter="10">
        <el-col :xs="12" :sm="6">
          <router-link to="/Gen/Chat/Index">
            <el-card>
              <el-row align="middle">
                <el-col :span="4">
                  <el-icon size="24">
                    <ChatDotRound />
                  </el-icon>
                </el-col>
                <el-col :span="20">
                  <el-row>
                    <el-text size="large">{{ t("Dashboard.GenChat") }}</el-text>
                  </el-row>
                  <el-row>
                    <el-text>{{ t("Dashboard.ChatDescription") }}</el-text>
                  </el-row>
                </el-col>
              </el-row>
            </el-card>
          </router-link>
        </el-col>
      </el-row>
    </el-card>
    <el-card class="mb-2">
      <el-row :gutter="10">
        <el-col :xs="12" :sm="6">
          <router-link to="/Image/SuperResolution/Index">
            <el-card>
              <el-row align="middle">
                <el-col :span="4">
                  <el-icon size="24">
                    <Picture />
                  </el-icon>
                </el-col>
                <el-col :span="20">
                  <el-row>
                    <el-text size="large">{{ t("Dashboard.ImageSuperResolution") }}</el-text>
                  </el-row>
                  <el-row>
                    <el-text>{{ t("Dashboard.ImageSuperResolutionDescription") }}</el-text>
                  </el-row>
                </el-col>
              </el-row>
            </el-card>
          </router-link>
        </el-col>
        <el-col :xs="12" :sm="6">
          <router-link to="/Image/AutoWipe/Index">
            <el-card>
              <el-row align="middle">
                <el-col :span="4">
                  <el-icon size="24">
                    <Picture />
                  </el-icon>
                </el-col>
                <el-col :span="20">
                  <el-row>
                    <el-text size="large">{{ t("Dashboard.ImageAutoWipe") }}</el-text>
                  </el-row>
                  <el-row>
                    <el-text>{{ t("Dashboard.ImageAutoWipeDescription") }}</el-text>
                  </el-row>
                </el-col>
              </el-row>
            </el-card>
          </router-link>
        </el-col>
        <el-col :xs="12" :sm="6">
          <router-link to="/Image/CartoonComic/Index">
            <el-card>
              <el-row align="middle">
                <el-col :span="4">
                  <el-icon size="24">
                    <Picture />
                  </el-icon>
                </el-col>
                <el-col :span="20">
                  <el-row>
                    <el-text size="large">{{ t("Dashboard.ImageCartoonComic") }}</el-text>
                  </el-row>
                  <el-row>
                    <el-text>{{ t("Dashboard.ImageCartoonComicDescription") }}</el-text>
                  </el-row>
                </el-col>
              </el-row>
            </el-card>
          </router-link>
        </el-col>
        <el-col :xs="12" :sm="6">
          <router-link to="/Image/Convert3d/Index">
            <el-card>
              <el-row align="middle">
                <el-col :span="4">
                  <el-icon size="24">
                    <Picture />
                  </el-icon>
                </el-col>
                <el-col :span="20">
                  <el-row>
                    <el-text size="large">{{ t("Dashboard.ImageConvert3d") }}</el-text>
                  </el-row>
                  <el-row>
                    <el-text>{{ t("Dashboard.ImageConvert3dDescription") }}</el-text>
                  </el-row>
                </el-col>
              </el-row>
            </el-card>
          </router-link>
        </el-col>
        <el-col :xs="12" :sm="6">
          <router-link to="/Image/ColorRestoration/Index">
            <el-card>
              <el-row align="middle">
                <el-col :span="4">
                  <el-icon size="24">
                    <Picture />
                  </el-icon>
                </el-col>
                <el-col :span="20">
                  <el-row>
                    <el-text size="large">{{ t("Dashboard.ImageColorRestoration") }}</el-text>
                  </el-row>
                  <el-row>
                    <el-text>{{ t("Dashboard.ImageColorRestorationDescription") }}</el-text>
                  </el-row>
                </el-col>
              </el-row>
            </el-card>
          </router-link>
        </el-col>
        <el-col :xs="12" :sm="6">
          <router-link to="/Image/FrameInterpolation/Index">
            <el-card>
              <el-row align="middle">
                <el-col :span="4">
                  <el-icon size="24">
                    <Picture />
                  </el-icon>
                </el-col>
                <el-col :span="20">
                  <el-row>
                    <el-text size="large">{{ t("Dashboard.ImageFrameInterpolation") }}</el-text>
                  </el-row>
                  <el-row>
                    <el-text>{{ t("Dashboard.ImageFrameInterpolationDescription") }}</el-text>
                  </el-row>
                </el-col>
              </el-row>
            </el-card>
          </router-link>
        </el-col>
        <el-col :xs="12" :sm="6">
          <router-link to="/Image/Matting/Index">
            <el-card>
              <el-row align="middle">
                <el-col :span="4">
                  <el-icon size="24">
                    <Picture />
                  </el-icon>
                </el-col>
                <el-col :span="20">
                  <el-row>
                    <el-text size="large">{{ t("Dashboard.ImageMatting") }}</el-text>
                  </el-row>
                  <el-row>
                    <el-text>{{ t("Dashboard.ImageMattingDescription") }}</el-text>
                  </el-row>
                </el-col>
              </el-row>
            </el-card>
          </router-link>
        </el-col>
        <el-col :xs="12" :sm="6">
          <router-link to="/Image/FaceRestoration/Index">
            <el-card>
              <el-row align="middle">
                <el-col :span="4">
                  <el-icon size="24">
                    <Picture />
                  </el-icon>
                </el-col>
                <el-col :span="20">
                  <el-row>
                    <el-text size="large">{{ t("Dashboard.ImageFaceRestoration") }}</el-text>
                  </el-row>
                  <el-row>
                    <el-text>{{ t("Dashboard.ImageFaceRestorationDescription") }}</el-text>
                  </el-row>
                </el-col>
              </el-row>
            </el-card>
          </router-link>
        </el-col>
      </el-row>
    </el-card>
    <el-card class="mb-2">
      <el-row :gutter="10">
        <el-col :xs="12" :sm="6">
          <router-link to="/Video/SuperResolution/Index">
            <el-card>
              <el-row align="middle">
                <el-col :span="4">
                  <el-icon size="24">
                    <VideoCamera />
                  </el-icon>
                </el-col>
                <el-col :span="20">
                  <el-row>
                    <el-text size="large">{{ t("Dashboard.VideoSuperResolution") }}</el-text>
                  </el-row>
                  <el-row>
                    <el-text>{{ t("Dashboard.VideoSuperResolutionDescription") }}</el-text>
                  </el-row>
                </el-col>
              </el-row>
            </el-card>
          </router-link>
        </el-col>
        <el-col :xs="12" :sm="6">
          <router-link to="/Video/AutoWipe/Index">
            <el-card>
              <el-row align="middle">
                <el-col :span="4">
                  <el-icon size="24">
                    <VideoCamera />
                  </el-icon>
                </el-col>
                <el-col :span="20">
                  <el-row>
                    <el-text size="large">{{ t("Dashboard.VideoAutoWipe") }}</el-text>
                  </el-row>
                  <el-row>
                    <el-text>{{ t("Dashboard.VideoAutoWipeDescription") }}</el-text>
                  </el-row>
                </el-col>
              </el-row>
            </el-card>
          </router-link>
        </el-col>
        <el-col :xs="12" :sm="6">
          <router-link to="/Video/CartoonComic/Index">
            <el-card>
              <el-row align="middle">
                <el-col :span="4">
                  <el-icon size="24">
                    <VideoCamera />
                  </el-icon>
                </el-col>
                <el-col :span="20">
                  <el-row>
                    <el-text size="large">{{ t("Dashboard.VideoCartoonComic") }}</el-text>
                  </el-row>
                  <el-row>
                    <el-text>{{ t("Dashboard.VideoCartoonComicDescription") }}</el-text>
                  </el-row>
                </el-col>
              </el-row>
            </el-card>
          </router-link>
        </el-col>
        <el-col :xs="12" :sm="6">
          <router-link to="/Video/Convert3d/Index">
            <el-card>
              <el-row align="middle">
                <el-col :span="4">
                  <el-icon size="24">
                    <VideoCamera />
                  </el-icon>
                </el-col>
                <el-col :span="20">
                  <el-row>
                    <el-text size="large">{{ t("Dashboard.VideoConvert3d") }}</el-text>
                  </el-row>
                  <el-row>
                    <el-text>{{ t("Dashboard.VideoConvert3dDescription") }}</el-text>
                  </el-row>
                </el-col>
              </el-row>
            </el-card>
          </router-link>
        </el-col>
        <el-col :xs="12" :sm="6">
          <router-link to="/Video/ColorRestoration/Index">
            <el-card>
              <el-row align="middle">
                <el-col :span="4">
                  <el-icon size="24">
                    <VideoCamera />
                  </el-icon>
                </el-col>
                <el-col :span="20">
                  <el-row>
                    <el-text size="large">{{ t("Dashboard.VideoColorRestoration") }}</el-text>
                  </el-row>
                  <el-row>
                    <el-text>{{ t("Dashboard.VideoColorRestorationDescription") }}</el-text>
                  </el-row>
                </el-col>
              </el-row>
            </el-card>
          </router-link>
        </el-col>
        <el-col :xs="12" :sm="6">
          <router-link to="/Video/FrameInterpolation/Index">
            <el-card>
              <el-row align="middle">
                <el-col :span="4">
                  <el-icon size="24">
                    <VideoCamera />
                  </el-icon>
                </el-col>
                <el-col :span="20">
                  <el-row>
                    <el-text size="large">{{ t("Dashboard.VideoFrameInterpolation") }}</el-text>
                  </el-row>
                  <el-row>
                    <el-text>{{ t("Dashboard.VideoFrameInterpolationDescription") }}</el-text>
                  </el-row>
                </el-col>
              </el-row>
            </el-card>
          </router-link>
        </el-col>
        <el-col :xs="12" :sm="6">
          <router-link to="/Video/Matting/Index">
            <el-card>
              <el-row align="middle">
                <el-col :span="4">
                  <el-icon size="24">
                    <VideoCamera />
                  </el-icon>
                </el-col>
                <el-col :span="20">
                  <el-row>
                    <el-text size="large">{{ t("Dashboard.VideoMatting") }}</el-text>
                  </el-row>
                  <el-row>
                    <el-text>{{ t("Dashboard.VideoMattingDescription") }}</el-text>
                  </el-row>
                </el-col>
              </el-row>
            </el-card>
          </router-link>
        </el-col>
        <el-col :xs="12" :sm="6">
          <router-link to="/Video/Organization/Index">
            <el-card>
              <el-row align="middle">
                <el-col :span="4">
                  <el-icon size="24">
                    <VideoCamera />
                  </el-icon>
                </el-col>
                <el-col :span="20">
                  <el-row>
                    <el-text size="large">{{ t("Dashboard.VideoOrganization") }}</el-text>
                  </el-row>
                  <el-row>
                    <el-text>{{ t("Dashboard.VideoOrganizationDescription") }}</el-text>
                  </el-row>
                </el-col>
              </el-row>
            </el-card>
          </router-link>
        </el-col>
      </el-row>
    </el-card>
    <el-card class="mb-2">
      <el-row :gutter="10">
        <el-col :xs="12" :sm="6">
          <router-link to="/Audio/VocalSplit/Index">
            <el-card>
              <el-row align="middle">
                <el-col :span="4">
                  <el-icon size="24">
                    <Headset />
                  </el-icon>
                </el-col>
                <el-col :span="20">
                  <el-row>
                    <el-text size="large">{{ t("Dashboard.AudioVocalSplit") }}</el-text>
                  </el-row>
                  <el-row>
                    <el-text>{{ t("Dashboard.AudioVocalSplitDescription") }}</el-text>
                  </el-row>
                </el-col>
              </el-row>
            </el-card>
          </router-link>
        </el-col>
        <el-col :xs="12" :sm="6">
          <router-link to="/Audio/Denoise/Index">
            <el-card>
              <el-row align="middle">
                <el-col :span="4">
                  <el-icon size="24">
                    <Headset />
                  </el-icon>
                </el-col>
                <el-col :span="20">
                  <el-row>
                    <el-text size="large">{{ t("Dashboard.AudioDenoise") }}</el-text>
                  </el-row>
                  <el-row>
                    <el-text>{{ t("Dashboard.AudioDenoiseDescription") }}</el-text>
                  </el-row>
                </el-col>
              </el-row>
            </el-card>
          </router-link>
        </el-col>
        <el-col :xs="12" :sm="6">
          <router-link to="/Audio/TTS/Index">
            <el-card>
              <el-row align="middle">
                <el-col :span="4">
                  <el-icon size="24">
                    <Headset />
                  </el-icon>
                </el-col>
                <el-col :span="20">
                  <el-row>
                    <el-text size="large">{{ t("Dashboard.AudioTTS") }}</el-text>
                  </el-row>
                  <el-row>
                    <el-text>{{ t("Dashboard.AudioTTSDescription") }}</el-text>
                  </el-row>
                </el-col>
              </el-row>
            </el-card>
          </router-link>
        </el-col>
        <el-col :xs="12" :sm="6">
          <router-link to="/Audio/STT/Index">
            <el-card>
              <el-row align="middle">
                <el-col :span="4">
                  <el-icon size="24">
                    <Headset />
                  </el-icon>
                </el-col>
                <el-col :span="20">
                  <el-row>
                    <el-text size="large">{{ t("Dashboard.AudioSTT") }}</el-text>
                  </el-row>
                  <el-row>
                    <el-text>{{ t("Dashboard.AudioSTTDescription") }}</el-text>
                  </el-row>
                </el-col>
              </el-row>
            </el-card>
          </router-link>
        </el-col>
      </el-row>
    </el-card>
    <el-card>
      <template #header>
        <el-text size="large">{{ t("Dashboard.Support") }}</el-text>
      </template>
      <el-space wrap :size="50">
        <el-text>Email: Rnchg@Hotmail.com</el-text>
        <el-text>Github: github.com/rnchg/AIPT</el-text>
        <el-text>Gitee: gitee.com/rnchg/AIPT</el-text>
        <el-text>Youtube: Light Cloud Wind</el-text>
        <el-text>Bilibili: 风轻云也净</el-text>
        <el-text>QQ: 6085398</el-text>
      </el-space>
    </el-card>
    <LicenseOrder v-model="licenseOrderVisible" />
  </div>
</template>

<script setup lang="ts">
import dashboard from "@/assets/images/dashboard.jpg";
import LicenseOrder from "@/views/License/Order.vue";
import API from "@/api/core.api";

defineOptions({
  name: "Dashboard",
  inheritAttrs: false,
});

const { t } = useI18n();

const licenseOrderVisible = ref(false);

onMounted(() => {
  API.validateApp().then((data) => {
    if (data.result) {
      return;
    }
    licenseOrderVisible.value = true;
  });
});
</script>

<style lang="scss" scoped>
.el-card :deep(.el-card__header) {
  padding: 10px;
}

.el-card :deep(.el-card__body) {
  padding: 10px;
}
</style>
