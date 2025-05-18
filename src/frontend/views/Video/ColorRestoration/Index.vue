<template>
  <div class="app-container">
    <el-card class="mb-2">
      <el-form ref="formRef" :model="formModel">
        <el-form-item :label="t('Video.ColorRestoration.InputFolder')" prop="input">
          <el-input
            v-model="formModel.input"
            :placeholder="t('Video.ColorRestoration.InputFolder')"
          >
            <template #append>
              <el-button @click="handleInput">
                {{ t("Video.ColorRestoration.InputSelect") }}
              </el-button>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item :label="t('Video.ColorRestoration.OutputFolder')" prop="output">
          <el-input
            v-model="formModel.output"
            :placeholder="t('Video.ColorRestoration.OutputFolder')"
          >
            <template #append>
              <el-button @click="handleOutput">
                {{ t("Video.ColorRestoration.OutputSelect") }}
              </el-button>
            </template>
          </el-input>
        </el-form-item>
        <el-space wrap :size="20">
          <el-form-item :label="t('Video.ColorRestoration.Provider')" prop="provider">
            <el-select v-model="formModel.provider" style="width: 500px">
              <el-option
                v-for="item in providerOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item :label="t('Video.ColorRestoration.Mode')" prop="mode">
            <el-select v-model="formModel.mode" style="width: 200px">
              <el-option
                v-for="item in modeOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item :label="t('Video.ColorRestoration.Quality')" prop="quality">
            <el-select v-model="formModel.quality" style="width: 200px">
              <el-option
                v-for="item in qualityOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
        </el-space>
        <el-form-item :label="t('Video.ColorRestoration.Progress')" prop="progress">
          <el-progress :percentage="progress" style="flex: 1" />
          <el-button type="primary" :loading="startLoading" @click="handleStart">
            {{ t("Video.ColorRestoration.Start") }}
          </el-button>
          <el-button type="danger" :disabled="stopDisabled" @click="handleStop">
            {{ t("Video.ColorRestoration.Stop") }}
          </el-button>
          <el-button type="success" @click="handleOpen">
            {{ t("Video.ColorRestoration.Open") }}
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
          <FileView ref="fileViewRef" :videoVisible="true" />
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
import API from "@/api/video/colorRestoration.api";

interface formType {
  input: string;
  output: string;
  input_files: string[];
  provider: string;
  mode: string;
  quality: string;
}

defineOptions({
  name: "VideoColorRestoration",
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
  quality: "",
});

const providerOptions = coreStore.providers;
const modeOptions = [{ value: "standard", label: t("Video.ColorRestoration.ModeStandard") }];
const qualityOptions = [
  { value: "high", label: t("Video.ColorRestoration.QualityHigh") },
  { value: "medium", label: t("Video.ColorRestoration.QualityMedium") },
  { value: "low", label: t("Video.ColorRestoration.QualityLow") },
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
    API.getFileUrl(val.path).then((data) => {
      fileViewRef.value.imageRef.src = data.url;
    });
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
  fileMessageRef.value.addMessage({ type: "info", text: t("Video.ColorRestoration.Help") });
});

onUnmounted(() => {
  API.setConfig(formModel);
});
</script>
