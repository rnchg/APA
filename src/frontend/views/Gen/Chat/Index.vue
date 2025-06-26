<template>
  <div v-loading="modelLoading" class="app-container" :element-loading-text="modelLoadingText">
    <el-card class="mb-2">
      <ChatView ref="chatViewRef" v-model:chat-message-data="chatMessageData" />
    </el-card>
    <el-card>
      <el-row>
        <el-col :span="12" class="text-left">
          <el-text>{{ promptInfo }}</el-text>
        </el-col>
        <el-col :span="12" class="text-right">
          <el-text>{{ promptLength }}</el-text>
        </el-col>
      </el-row>
      <el-row class="mb-2">
        <el-input
          v-model="prompt"
          type="textarea"
          :maxlength="formModel.prompt_max_length"
          autosize
          @keydown.enter="handleSendKeydown"
        />
      </el-row>
      <el-row>
        <el-col :span="10">
          <el-button type="default" round>{{ t("Gen.Chat.Image") }}</el-button>
          <el-button type="default" round>{{ t("Gen.Chat.Video") }}</el-button>
          <el-button type="default" round>{{ t("Gen.Chat.Audio") }}</el-button>
        </el-col>
        <el-col :span="10" class="text-right">
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
        <el-col :span="4" class="text-right">
          <el-checkbox
            v-model="think"
            :label="t('Gen.Chat.Think')"
            :disabled="sendDisabled"
            border
          />
        </el-col>
      </el-row>
    </el-card>
    <Config v-model="configVisible" @save="handleConfigSave" />
    <LicenseOrder v-model="licenseOrderVisible" />
  </div>
</template>
<script setup lang="ts">
import LicenseOrder from "@/views/License/Order.vue";
import ChatView, { Message } from "@/views/Component/ChatView.vue";
import Config from "@/views/Gen/Chat/Config.vue";
import { assignUpdate } from "@/utils";
import API from "@/api/gen/chat.api";

interface formType {
  prompt_system: string;
  prompt_max_length: number;
  context_max_length: number;
}

defineOptions({
  name: "GenChat",
  inheritAttrs: false,
});

const { t } = useI18n();

const licenseOrderVisible = ref(false);

const modelLoading = ref(false);
const modelLoadingText = ref(t("Gen.Chat.ModelInitWait"));

const formModel = reactive<formType>({
  prompt_system: "",
  prompt_max_length: 0,
  context_max_length: 0,
});

const think = ref(false);

const prompt = ref("");

const promptInfo = ref("");
const promptLength = ref("");

const sendDisabled = ref(false);

const chatViewRef = ref();

const chatMessageData = ref<Message[]>([]);

const configVisible = ref(false);

function handleInitModel() {
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

function handleInitConfig() {
  API.getConfig().then((data) => {
    assignUpdate(formModel, { ...data });
    handlePromptLength();
  });
}

function handlePromptLength() {
  promptLength.value = `[ ${prompt.value.length}/${formModel.prompt_max_length} ]`;
}

function handleBegin() {
  prompt.value = "";
  sendDisabled.value = true;
  promptInfo.value = t("Gen.Chat.ModelProcessWait");
}

function handleEnd() {
  sendDisabled.value = false;
  promptInfo.value = t("Gen.Chat.InputPrompt");
}

function handleSendKeydown(event: any) {
  if (event.ctrlKey && event.key === "Enter") {
    handleSend();
  }
}

function handleSend() {
  if (prompt.value.trim().length === 0) {
    ElMessage.error(t("Gen.Chat.InputPromptEmpty"));
    return;
  }
  const [promptList, thinkMessage, assistantMessage] = chatViewRef.value.sendAndBuildMessage(
    prompt.value,
    think.value
  );
  handleBegin();
  API.start(
    {
      prompt: promptList,
      think: think.value,
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
        chatViewRef.value.addToken(data.token, think.value, thinkMessage, assistantMessage);
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

function handleConfigSave() {
  handleInitConfig();
}

watch([prompt], () => handlePromptLength());

onMounted(() => {
  chatViewRef.value.addMessage({ type: "System", text: t("Gen.Chat.Help") });
  promptInfo.value = t("Gen.Chat.InputPrompt");
  handleInitConfig();
  handleInitModel();
});
</script>
