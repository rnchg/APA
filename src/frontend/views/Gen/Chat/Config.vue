<template>
  <div>
    <el-dialog v-model="visible" :title="t('Gen.Chat.ConfigTitle')" width="75%">
      <el-card class="mb-2">
        <template #header>
          <el-text>{{ t("Gen.Chat.ConfigPromptSystem") }}</el-text>
        </template>
        <el-input
          v-model="formModel.prompt_system"
          type="textarea"
          :rows="10"
          style="width: 100%"
        />
      </el-card>
      <el-card class="mb-2">
        <template #header>
          <el-text>{{ t("Gen.Chat.ConfigPromptMaxLength") }}</el-text>
        </template>
        <el-input-number v-model="formModel.prompt_max_length" :min="1" :max="4096" :step="1" />
      </el-card>
      <el-card>
        <template #header>
          <el-text>{{ t("Gen.Chat.ConfigContextMaxLength") }}</el-text>
        </template>
        <el-input-number v-model="formModel.context_max_length" :min="1" :max="100" :step="1" />
      </el-card>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="handleSave">{{ t("Gen.Chat.ConfigSave") }}</el-button>
          <el-button type="danger" @click="handleClose">{{ t("Gen.Chat.ConfigClose") }}</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { assignUpdate } from "@/utils";
import API from "@/api/gen/chat.api";

interface formType {
  prompt_system: string;
  prompt_max_length: number;
  context_max_length: number;
}

const visible = defineModel("modelValue", {
  type: Boolean,
  default: false,
  required: true,
});

const emit = defineEmits(["getRequestCode", "save", "close"]);

const { t } = useI18n();

const formModel = reactive<formType>({
  prompt_system: "",
  prompt_max_length: 0,
  context_max_length: 0,
});

function handleSave() {
  API.setConfig(formModel).then(() => {
    visible.value = false;
    emit("save");
    ElMessage.success("操作成功");
  });
}

function handleClose() {
  visible.value = false;
  emit("close");
}

watch(visible, (newValue) => {
  if (newValue) {
    API.getConfig().then((data) => assignUpdate(formModel, { ...data }));
  }
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
