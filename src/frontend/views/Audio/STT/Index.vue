<template>
  <div class="app-container">
    <el-card class="mb-2">
      <el-form ref="formRef" :model="formModel">
        <el-form-item :label="t('Audio.STT.InputFolder')" prop="input">
          <el-input v-model="formModel.input" :placeholder="t('Audio.STT.InputFolder')">
            <template #append>
              <el-button @click="handleInput">
                {{ t("Audio.STT.InputSelect") }}
              </el-button>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item :label="t('Audio.STT.OutputFolder')" prop="output">
          <el-input v-model="formModel.output" :placeholder="t('Audio.STT.OutputFolder')">
            <template #append>
              <el-button @click="handleOutput">
                {{ t("Audio.STT.OutputSelect") }}
              </el-button>
            </template>
          </el-input>
        </el-form-item>
        <el-space wrap :size="20">
          <el-form-item :label="t('Audio.STT.Provider')" prop="provider">
            <el-select v-model="formModel.provider" style="width: 500px">
              <el-option
                v-for="item in providerOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item :label="t('Audio.STT.Mode')" prop="mode">
            <el-select v-model="formModel.mode" style="width: 200px">
              <el-option
                v-for="item in modeOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item :label="t('Audio.STT.Lang')" prop="language">
            <el-select v-model="formModel.lang" style="width: 200px">
              <el-option
                v-for="item in langOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="相似阈值" prop="similarity">
            <el-slider
              v-model="formModel.similarity"
              :min="0"
              :max="1"
              :step="0.01"
              style="width: 200px"
            />
          </el-form-item>
        </el-space>
        <el-form-item :label="t('Audio.STT.Progress')" prop="progress">
          <el-progress :percentage="progress" style="flex: 1" />
          <el-button type="primary" :loading="startLoading" @click="handleStart">
            {{ t("Audio.STT.Start") }}
          </el-button>
          <el-button type="danger" :disabled="stopDisabled" @click="handleStop">
            {{ t("Audio.STT.Stop") }}
          </el-button>
          <el-button type="success" @click="handleOpen">
            {{ t("Audio.STT.Open") }}
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
import API from "@/api/audio/stt.api";

interface formType {
  input: string;
  output: string;
  input_files: string[];
  provider: string;
  mode: string;
  lang: number;
  similarity: number;
}

defineOptions({
  name: "AudioSTT",
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
  lang: 0,
  similarity: 0,
});

const providerOptions = coreStore.providers;
const modeOptions = [{ value: "standard", label: t("Audio.STT.ModeStandard") }];
const langOptions = [
  { value: 0, label: t("Audio.STT.LangAuto") },
  { value: 1, label: t("Audio.STT.LangEn") },
  { value: 2, label: t("Audio.STT.LangZh") },
  { value: 3, label: t("Audio.STT.LangYue") },
  { value: 4, label: t("Audio.STT.LangJa") },
  { value: 5, label: t("Audio.STT.LangKo") },
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

const audioVisible = ref(true);
const textVisible = ref(false);

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
      API.getFileUrl(val.path).then((data) => {
        textVisible.value = false;
        audioVisible.value = true;
        nextTick(() => (fileViewRef.value.audioRef.src = data.url));
      });
    } else if (fileSwitchItem.value === "output") {
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
  fileMessageRef.value.addMessage({ type: "info", text: t("Audio.STT.Help") });
});

onUnmounted(() => {
  API.setConfig(formModel);
});
</script>
