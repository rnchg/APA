<template>
  <div class="app-container">
    <el-card class="mb-2">
      <el-form ref="formRef" :model="formModel">
        <el-form-item :label="t('Audio.TTS.InputFolder')" prop="input">
          <el-input v-model="formModel.input" :placeholder="t('Audio.TTS.InputFolder')">
            <template #append>
              <el-button @click="handleInput">
                {{ t("Audio.TTS.InputSelect") }}
              </el-button>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item :label="t('Audio.TTS.OutputFolder')" prop="output">
          <el-input v-model="formModel.output" :placeholder="t('Audio.TTS.OutputFolder')">
            <template #append>
              <el-button @click="handleOutput">
                {{ t("Audio.TTS.OutputSelect") }}
              </el-button>
            </template>
          </el-input>
        </el-form-item>
        <el-space wrap :size="20">
          <el-form-item :label="t('Audio.TTS.Provider')" prop="provider">
            <el-select v-model="formModel.provider" style="width: 500px">
              <el-option
                v-for="item in providerOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item :label="t('Audio.TTS.Mode')" prop="mode">
            <el-select v-model="formModel.mode" style="width: 200px">
              <el-option
                v-for="item in modeOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item :label="t('Audio.TTS.Voice')" prop="voice">
            <el-select v-model="formModel.voice" style="width: 200px">
              <el-option
                v-for="item in voiceOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
        </el-space>
        <el-form-item :label="t('Audio.TTS.Progress')" prop="progress">
          <el-progress :percentage="progress" style="flex: 1" />
          <el-button type="primary" :loading="startLoading" @click="handleStart">
            {{ t("Audio.TTS.Start") }}
          </el-button>
          <el-button type="danger" :disabled="stopDisabled" @click="handleStop">
            {{ t("Audio.TTS.Stop") }}
          </el-button>
          <el-button type="success" @click="handleOpen">
            {{ t("Audio.TTS.Open") }}
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
    <el-row :gutter="10">
      <el-col :sm="6">
        <el-card class="mb-2">
          <FileGrid
            ref="fileGridRef"
            v-model:fileSwitchItem="fileSwitchItem"
            v-model:fileTableRow="fileTableRow"
            :fileTableData="fileTableData"
            @table-change="handlefileGridTable"
          />
        </el-card>
      </el-col>
      <el-col :sm="12">
        <el-card class="mb-2">
          <FileView ref="fileViewRef" :audioVisible="audioVisible" :textVisible="textVisible" />
        </el-card>
      </el-col>
      <el-col :sm="6">
        <el-card>
          <FileMessage ref="fileMessageRef" v-model:fileMessageData="fileMessageData" />
        </el-card>
      </el-col>
    </el-row>
    <LicenseOrder v-model="licenseOrderVisible" />
  </div>
</template>
<script setup lang="ts">
import { assignUpdate } from "@/utils";
import { useCoreStore } from "@/store";
import LicenseOrder from "@/views/License/Order.vue";
import FileGrid, { FileTable } from "@/views/Component/FileGrid.vue";
import FileView from "@/views/Component/FileView.vue";
import FileMessage, { Message } from "@/views/Component/FileMessage.vue";
import API from "@/api/audio/tts.api";

interface formType {
  input: string;
  output: string;
  input_files: string[];
  provider: string;
  mode: string;
  voice: string;
}

defineOptions({
  name: "AudioTTS",
  inheritAttrs: false,
});

const { t } = useI18n();

const coreStore = useCoreStore();

const licenseOrderVisible = ref(false);

const formRef = ref();
const formModel = reactive<formType>({
  input: "",
  output: "",
  input_files: [],
  provider: "",
  mode: "",
  voice: "",
});

const providerOptions = coreStore.providers;
const modeOptions = [{ value: "standard", label: t("Audio.TTS.ModeStandard") }];
const voiceOptions = [
  { value: "af_maple", label: "[ af_maple ]" },
  { value: "af_sol", label: "[ af_sol ]" },
  { value: "bf_vale", label: "[ bf_vale ]" },
  { value: "zf_001", label: "[ zf_001 ]" },
  { value: "zf_002", label: "[ zf_002 ]" },
  { value: "zf_003", label: "[ zf_003 ]" },
  { value: "zf_004", label: "[ zf_004 ]" },
  { value: "zf_005", label: "[ zf_005 ]" },
  { value: "zf_006", label: "[ zf_006 ]" },
  { value: "zf_007", label: "[ zf_007 ]" },
  { value: "zf_008", label: "[ zf_008 ]" },
  { value: "zf_017", label: "[ zf_017 ]" },
  { value: "zf_018", label: "[ zf_018 ]" },
  { value: "zm_009", label: "[ zm_009 ]" },
  { value: "zm_010", label: "[ zm_010 ]" },
  { value: "zm_011", label: "[ zm_011 ]" },
  { value: "zm_012", label: "[ zm_012 ]" },
  { value: "zm_013", label: "[ zm_013 ]" },
  { value: "zm_014", label: "[ zm_014 ]" },
  { value: "zm_015", label: "[ zm_015 ]" },
  { value: "zm_016", label: "[ zm_016 ]" },
  { value: "zm_020", label: "[ zm_020 ]" },
  { value: "zm_025", label: "[ zm_025 ]" },
];

const progress = ref(0);

const startLoading = ref(false);
const stopDisabled = ref(true);

const fileGridRef = ref();
const fileSwitchItem = ref("input");
const fileTableData = ref<FileTable[]>([]);
const fileTableRow = ref<FileTable>();

const fileViewRef = ref();

const fileMessageRef = ref();
const fileMessageData = ref<Message[]>([]);

const audioVisible = ref(false);
const textVisible = ref(true);

function handleInput() {
  API.getFolder(formModel.input).then((data) => {
    formModel.input = data.folder;
  });
}

function handleOutput() {
  API.getFolder(formModel.output).then((data) => {
    formModel.output = data.folder;
  });
}

function setFileGrid() {
  let folder = undefined;
  if (formModel.input && fileSwitchItem.value === "input") {
    folder = formModel.input;
  }
  if (formModel.output && fileSwitchItem.value === "output") {
    folder = formModel.output;
  }
  if (folder === undefined) {
    fileTableData.value = [];
    return;
  }
  API.getFileGrid(folder, fileSwitchItem.value).then((data) => {
    if (!data.files) {
      return;
    }
    fileTableData.value = data.files;
    const prevFile = fileTableRow.value?.basename;
    if (prevFile) {
      const currFile = fileTableData.value.find((e) => e.basename === prevFile);
      if (currFile) {
        fileGridRef.value.fileTableRef.setCurrentRow(currFile);
        return;
      }
    }
    fileGridRef.value.fileTableRef.setCurrentRow(fileTableData.value[0]);
  });
}

function handlefileGridTable(val: FileTable | undefined) {
  if (val) {
    if (fileSwitchItem.value === "input") {
      API.getFileView(val.path).then((data) => {
        audioVisible.value = false;
        textVisible.value = true;
        nextTick(() => {
          const reader = new FileReader();
          reader.readAsText(data.data);
          reader.onload = () => {
            fileViewRef.value.textVal = reader.result;
          };
        });
      });
    } else if (fileSwitchItem.value === "output") {
      API.getFileUrl(val.path).then((data) => {
        textVisible.value = false;
        audioVisible.value = true;
        nextTick(() => (fileViewRef.value.audioRef.src = data.url));
      });
    }
  }
}

function handleBegin() {
  startLoading.value = true;
  stopDisabled.value = false;
  progress.value = 0;
}

function handleEnd() {
  startLoading.value = false;
  stopDisabled.value = true;
  progress.value = 0;
}

function handleStart() {
  formModel.input_files = fileTableData.value.map((e) => e.path);
  handleBegin();
  API.start(
    formModel,
    (msg: any) => {
      const data = JSON.parse(msg.data);
      progress.value = data.progress * 100;
      if (!data.is_auth) {
        handleEnd();
        licenseOrderVisible.value = true;
      }
      if (data.is_stop) {
        handleEnd();
      }
      if (data.message) {
        fileMessageRef.value.addMessage(data.message);
      }
    },
    (err: any) => {
      ElMessage.error(err.message);
      handleEnd();
    }
  );
}

function handleStop() {
  API.stop().then(() => handleBegin());
}

function handleOpen() {
  API.open(formModel.output);
}

watch([() => formModel.input, () => formModel.output, fileSwitchItem], () => setFileGrid());

onMounted(() => {
  API.getConfig().then((data) => assignUpdate(formModel, { ...data }));
  fileMessageRef.value.addMessage({ type: "info", text: t("Audio.TTS.Help") });
});

onUnmounted(() => {
  API.setConfig(formModel);
});
</script>
