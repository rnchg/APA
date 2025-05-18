<template>
  <div class="app-container" v-loading="modelLoading" :element-loading-text="modelLoadingText">
    <el-card class="mb-2">
      <ChatView ref="chatViewRef" v-model:chatMessageData="chatMessageData" />
    </el-card>
    <el-card>
      <el-row class="mb-2">
        <el-input
          v-model="prompt"
          :placeholder="placeholder"
          type="textarea"
          autosize
          @keydown.enter="handleSendKeydown"
        />
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-button type="default" round>{{ t("Gen.Chat.Image") }}</el-button>
          <el-button type="default" round>{{ t("Gen.Chat.Video") }}</el-button>
          <el-button type="default" round>{{ t("Gen.Chat.Audio") }}</el-button>
        </el-col>
        <el-col :span="12" class="text-right">
          <el-button type="success" round @click="handleConfig">
            {{ t("Gen.Chat.Config") }}
          </el-button>
          <el-button type="warning" round @click="handleReset">{{ t("Gen.Chat.Reset") }}</el-button>
          <el-button type="danger" round @click="handleCancel">
            {{ t("Gen.Chat.Cancel") }}
          </el-button>
          <el-button type="primary" round :disabled="sendDisabled" @click="handleSend">
            {{ t("Gen.Chat.Send") }}
          </el-button>
        </el-col>
      </el-row>
    </el-card>
    <Config v-model="configVisible" />
    <LicenseOrder v-model="licenseOrderVisible" />
  </div>
</template>
<script setup lang="ts">
import LicenseOrder from "@/views/License/Order.vue";
import ChatView, { Message } from "@/views/Component/ChatView.vue";
import Config from "@/views/Gen/Chat/Config.vue";
import API from "@/api/gen/chat.api";

defineOptions({
  name: "GenChat",
  inheritAttrs: false,
});

const { t } = useI18n();

const licenseOrderVisible = ref(false);

const modelLoading = ref(false);
const modelLoadingText = ref(t("Gen.Chat.ModelInitWait"));

const prompt = ref("");
const placeholder = ref("");
const sendDisabled = ref(false);

const chatViewRef = ref();

const chatMessageData = ref<Message[]>([]);

const configVisible = ref(false);

function handleInit() {
  API.getInit().then((data) => {
    if (data.is_init) {
      return;
    }
    modelLoading.value = true;
    API.init(
      {},
      function (msg: any) {
        const data = JSON.parse(msg.data);
        if (!data.is_auth) {
          modelLoading.value = false;
          licenseOrderVisible.value = true;
        }
        if (!data.is_init) {
          modelLoading.value = false;
        }
        if (data.message) {
          ElMessage.error(data.message.text);
        }
      },
      function (err: any) {
        ElMessage.error(err.message);
        modelLoading.value = false;
      }
    );
  });
}

function handleBegin() {
  prompt.value = "";
  sendDisabled.value = true;
}

function handleEnd() {
  sendDisabled.value = false;
}

function handleSendKeydown(event: any) {
  if (event.ctrlKey && event.code === "Enter") {
    handleSend();
  }
}

function handleSend() {
  if (!prompt.value) {
    ElMessage.error(t("Gen.Chat.InputPromptEmpty"));
    return;
  }
  const [promptText, assistant] = chatViewRef.value.sendAndBuildMessage({
    type: "User",
    text: prompt.value,
  });
  handleBegin();
  API.start(
    {
      prompt: promptText,
    },
    function (msg: any) {
      const data = JSON.parse(msg.data);
      if (!data.is_auth) {
        handleEnd();
        licenseOrderVisible.value = true;
      }
      if (data.is_stop) {
        handleEnd();
      }
      if (data.message) {
        ElMessage.error(data.message.text);
      }
      if (data.token) {
        chatViewRef.value.addToken(assistant, data.token);
      }
    },
    function (err: any) {
      ElMessage.error(err.message);
      handleEnd();
    }
  );
}

function handleCancel() {
  API.stop().then(() => {
    chatViewRef.value.cancelMessage();
  });
}

function handleReset() {
  API.stop().then(() => {
    chatViewRef.value.resetMessage();
  });
}

function handleConfig() {
  configVisible.value = true;
}

onMounted(() => {
  chatViewRef.value.addMessage({ type: "System", text: t("Gen.Chat.Help") });
  handleInit();
});
</script>
