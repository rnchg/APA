<template>
  <div class="app-container">
    <el-card class="mb-2">
      <el-form ref="formRef" :model="formModel">
        <el-form-item :label="t('Image.CartoonComic.InputFolder')" prop="input">
          <el-input v-model="formModel.input" :placeholder="t('Image.CartoonComic.InputFolder')">
            <template #append>
              <el-button type="primary" @click="handleInput">
                {{ t("Image.CartoonComic.InputSelect") }}
              </el-button>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item :label="t('Image.CartoonComic.OutputFolder')" prop="output">
          <el-input v-model="formModel.output" :placeholder="t('Image.CartoonComic.OutputFolder')">
            <template #append>
              <el-button type="primary" @click="handleOutput">
                {{ t("Image.CartoonComic.OutputSelect") }}
              </el-button>
            </template>
          </el-input>
        </el-form-item>
        <el-space wrap :size="20">
          <el-form-item :label="t('Image.CartoonComic.Provider')" prop="provider">
            <el-select v-model="formModel.provider" style="width: 500px">
              <el-option
                v-for="item in providerOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item :label="t('Image.CartoonComic.Mode')" prop="mode">
            <el-select v-model="formModel.mode" style="width: 200px">
              <el-option
                v-for="item in modeOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item :label="t('Image.CartoonComic.Quality')" prop="quality">
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
        <el-form-item :label="t('Image.CartoonComic.Progress')" prop="progress">
          <el-progress :percentage="progress" style="flex: 1" />
          <el-button type="primary" :loading="startLoading" @click="handleStart">
            {{ t("Image.CartoonComic.Start") }}
          </el-button>
          <el-button type="danger" :disabled="stopDisabled" @click="handleStop">
            {{ t("Image.CartoonComic.Stop") }}
          </el-button>
          <el-button type="success" @click="handleOpen">
            {{ t("Image.CartoonComic.Open") }}
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
    <el-row :gutter="10">
      <el-col :sm="6">
        <el-card class="mb-2">
          <FileGrid
            ref="fileGridRef"
            v-model:switch-item="fileGridSwitchItem"
            v-model:table-item="fileGridTableItem"
            :table-list="fileGridTableList"
            @table-change="handlefileGridTable"
          />
        </el-card>
      </el-col>
      <el-col :sm="12">
        <el-card class="mb-2">
          <FileView ref="fileViewRef" :image-visible="true" />
        </el-card>
      </el-col>
      <el-col :sm="6">
        <el-card>
          <FileMessage ref="fileMessageRef" v-model:message-list="fileMessageList" />
        </el-card>
      </el-col>
    </el-row>
    <LicenseOrder v-model="licenseOrderVisible" />
  </div>
</template>
<script setup lang="ts">
import { assignUpdate } from "@/utils";
import { useCoreStore } from "@/store";
import { FileSwitchEnum, MessageTypeEnum } from "@/enums/const/view.enum";
import LicenseOrder from "@/views/License/Order.vue";
import FileGrid, { FileTable } from "@/views/Component/FileGrid.vue";
import FileView from "@/views/Component/FileView.vue";
import FileMessage, { Model } from "@/views/Component/FileMessage.vue";
import API from "@/api/image/cartoonComic-api";

interface formType {
  input: string;
  output: string;
  input_files: string[];
  provider: string;
  mode: string;
  quality: string;
}

defineOptions({
  name: "ImageCartoonComic",
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
const modeOptions = [
  { value: "hayao", label: t("Image.CartoonComic.ModeHayao") },
  { value: "cute", label: t("Image.CartoonComic.ModeCute") },
  { value: "jpface", label: t("Image.CartoonComic.ModeJPFace") },
  { value: "ghibli", label: t("Image.CartoonComic.ModeGhibli") },
  { value: "shinkai", label: t("Image.CartoonComic.ModeShinkai") },
  { value: "sketch", label: t("Image.CartoonComic.ModeSketch") },
];
const qualityOptions = [
  { value: "auto", label: t("Image.CartoonComic.QualityAuto") },
  { value: "high", label: t("Image.CartoonComic.QualityHigh") },
  { value: "medium", label: t("Image.CartoonComic.QualityMedium") },
  { value: "low", label: t("Image.CartoonComic.QualityLow") },
];

const progress = ref(0);

const startLoading = ref(false);
const stopDisabled = ref(true);

const fileGridRef = ref();
const fileGridSwitchItem = ref(FileSwitchEnum.Input);
const fileGridTableList = ref<FileTable[]>([]);
const fileGridTableItem = ref<FileTable>();

const fileViewRef = ref();

const fileMessageRef = ref();
const fileMessageList = ref<Model[]>([]);

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
  if (formModel.input && fileGridSwitchItem.value === FileSwitchEnum.Input) {
    folder = formModel.input;
  }
  if (formModel.output && fileGridSwitchItem.value === FileSwitchEnum.Output) {
    folder = formModel.output;
  }
  if (folder === undefined) {
    fileGridTableList.value = [];
    return;
  }
  API.getFileGrid(folder, fileGridSwitchItem.value).then((data) => {
    if (data.files === undefined || data.files.length === 0) {
      fileGridTableList.value = [];
      return;
    }
    fileGridTableList.value = data.files;
    const prevFile = fileGridTableItem.value?.basename;
    if (prevFile) {
      const currFile = fileGridTableList.value.find((e) => e.basename === prevFile);
      if (currFile) {
        fileGridRef.value.tableRef.setCurrentRow(currFile);
        return;
      }
    }
    fileGridRef.value.tableRef.setCurrentRow(fileGridTableList.value[0]);
  });
}

function handlefileGridTable(val: FileTable | undefined) {
  if (val) {
    API.getFileUrl(val.path).then((data) => fileViewRef.value.setImageSrc(data.url));
  } else {
    fileViewRef.value.setImageSrc("");
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
  formModel.input_files = fileGridTableList.value.map((e) => e.path);
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

watch([() => formModel.input, () => formModel.output, fileGridSwitchItem], () => setFileGrid());

watch(formModel, () => API.setConfig(formModel));

onMounted(() => {
  API.getConfig().then((data) => assignUpdate(formModel, { ...data }));
  fileMessageRef.value.addMessage({
    type: MessageTypeEnum.Info,
    text: t("Image.CartoonComic.Help"),
  });
});

onUnmounted(() => {
  API.setConfig(formModel);
});
</script>
