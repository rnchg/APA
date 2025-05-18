<template>
  <div class="app-container">
    <el-card class="mb-2">
      <el-form ref="formRef" :model="formModel">
        <el-form-item :label="t('Video.Convert3d.InputFolder')" prop="input">
          <el-input v-model="formModel.input" :placeholder="t('Video.Convert3d.InputFolder')">
            <template #append>
              <el-button @click="handleInput">
                {{ t("Video.Convert3d.InputSelect") }}
              </el-button>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item :label="t('Video.Convert3d.OutputFolder')" prop="output">
          <el-input v-model="formModel.output" :placeholder="t('Video.Convert3d.OutputFolder')">
            <template #append>
              <el-button @click="handleOutput">
                {{ t("Video.Convert3d.OutputSelect") }}
              </el-button>
            </template>
          </el-input>
        </el-form-item>
        <el-space wrap :size="20">
          <el-form-item :label="t('Video.Convert3d.Provider')" prop="provider">
            <el-select v-model="formModel.provider" style="width: 500px">
              <el-option
                v-for="item in providerOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item :label="t('Video.Convert3d.Mode')" prop="mode">
            <el-select v-model="formModel.mode" style="width: 150px">
              <el-option
                v-for="item in modeOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item :label="t('Video.Convert3d.Format')" prop="format">
            <el-select v-model="formModel.format" style="width: 150px">
              <el-option
                v-for="item in formatOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item :label="t('Video.Convert3d.Shift')" prop="shift">
            <el-select v-model="formModel.shift" style="width: 100px">
              <el-option
                v-for="item in shiftOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item :label="t('Video.Convert3d.PopOut')" prop="popOut">
            <el-switch v-model="formModel.pop_out" style="width: 50px" />
          </el-form-item>
          <el-form-item :label="t('Video.Convert3d.CrossEye')" prop="crossEye">
            <el-switch v-model="formModel.cross_eye" style="width: 50px" />
          </el-form-item>
        </el-space>
        <el-form-item :label="t('Video.Convert3d.Progress')" prop="progress">
          <el-progress :percentage="progress" style="flex: 1" />
          <el-button type="primary" :loading="startLoading" @click="handleStart">
            {{ t("Video.Convert3d.Start") }}
          </el-button>
          <el-button type="danger" :disabled="stopDisabled" @click="handleStop">
            {{ t("Video.Convert3d.Stop") }}
          </el-button>
          <el-button type="success" @click="handleOpen">
            {{ t("Video.Convert3d.Open") }}
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
import API from "@/api/video/convert3d.api";

interface formType {
  input: string;
  output: string;
  input_files: string[];
  provider: string;
  mode: string;
  format: string;
  shift: string;
  pop_out: boolean;
  cross_eye: boolean;
}

defineOptions({
  name: "VideoConvert3d",
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
  format: "",
  shift: "",
  pop_out: false,
  cross_eye: false,
});

const providerOptions = coreStore.providers;
const modeOptions = [{ value: "standard", label: t("Video.Convert3d.ModeStandard") }];
const formatOptions = [
  { value: "half_sbs", label: t("Video.Convert3d.FormatHalfSbs") },
  { value: "sbs", label: t("Video.Convert3d.FormatSbs") },
  { value: "anaglyph", label: t("Video.Convert3d.FormatAnaglyph") },
  { value: "depth", label: t("Video.Convert3d.FormatDepth") },
];
const shiftOptions = [
  { value: "10", label: t("Video.Convert3d.Shift10") },
  { value: "20", label: t("Video.Convert3d.Shift20") },
  { value: "30", label: t("Video.Convert3d.Shift30") },
  { value: "50", label: t("Video.Convert3d.Shift50") },
  { value: "100", label: t("Video.Convert3d.Shift100") },
  { value: "200", label: t("Video.Convert3d.Shift200") },
  { value: "300", label: t("Video.Convert3d.Shift300") },
  { value: "500", label: t("Video.Convert3d.Shift500") },
  { value: "1000", label: t("Video.Convert3d.Shift1000") },
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
  fileMessageRef.value.addMessage({ type: "info", text: t("Video.Convert3d.Help") });
});

onUnmounted(() => {
  API.setConfig(formModel);
});
</script>
