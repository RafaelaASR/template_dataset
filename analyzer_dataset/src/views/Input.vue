<script setup>
import { ref, defineEmits } from 'vue';

import { executarAnalise } from '@/api'

const test = ref(20);
const custom = ref(false);
const parametros = ref(null);
const emits = defineEmits(['update:result']);
const isLoading = ref(false);

const error = ref('')
const status = ref('idle')
const arquivo = ref(null)
const method = ref('gradient_boosting');









// ********************************************
// APENAS remova '//' da frente do seu método
// ********************************************
const methods = [
  { label: 'Gradient Boosting', value: 'gradient_boosting' },
  //{ label: 'Lasso', value: 'lasso' },
  //{ label: 'Bagging', value: 'bagging' },
  //{ label: 'SVR', value: 'svr' },
  //{ label: 'Huber Regressor', value: 'huber_regressor' },
  //{ label: 'KNN', value: 'knn' },
  //{ label: 'Extra Trees', value: 'extra_trees' },
  //{ label: 'Ridge', value: 'ridge' },
  //{ label: 'SGD Regressor', value: 'sgd_regressor' },
  //{ label: 'Bayesian Ridge', value: 'bayesian_ridge' },
  //{ label: 'Decision Tree', value: 'decision_tree' },
  //{ label: 'Regressão Linear', value: 'regressao_linear' },
  //{ label: 'HistGradientBoosting', value: 'hist_gradient_boosting' },
  //{ label: 'Kernel Ridge', value: 'kernel_ridge' },
  //{ label: 'AdaBoost', value: 'adaboost' },
  //{ label: 'Elastic Net', value: 'elastic_net' },
  //{ label: 'Random Forest', value: 'random_forest' },
];














































async function executar() {
  if (!arquivo.value) return

  error.value = ''
  status.value = 'reading'
  isLoading.value = true
  emits('update:loading', true)

  try {
    const dados = await executarAnalise(
      arquivo.value,
      method.value,
      custom.value ? parametros.value : null,
      test.value / 100,
    )

    emits('update:result', dados)
  } catch (e) {
    error.value = e.response?.data?.detail ?? e.message
  } finally {
    isLoading.value = false
    emits('update:loading', false)
    status.value = 'idle'
  }
}

</script>

<template>
  <div class="layout">
    <aside class="sidebar d-flex flex-column">
      <div class="d-flex align-center ga-2 text-body-2 font-weight-bold">
        <v-icon icon="mdi-tune" size="16" /><span>Configuração</span>
      </div>

      <v-file-upload
        v-model="arquivo"
        accept=".csv"
        hide-browse
        divider=""
        :disabled="status === 'reading'"
        class="upload-box"
        density="compact" 
        @update:model-value="onArquivo"
        >
        <template #icon>
          <span v-if="!arquivo" class="upload-icon">
            <v-icon :icon="arquivo ? 'mdi-file-document-outline' : 'mdi-tray-arrow-up'" size="22" />
          </span>
        </template>

        <template #title>
          <div v-if="arquivo" class="arquivo-info">
            <span class="arquivo-nome">{{ arquivo.name }}</span>
            <span class="arquivo-tipo">{{ arquivo.type || 'texto' }}</span>
          </div>
          <span v-else class="font-weight-bold">Adicionar dataset</span>
        </template>
      </v-file-upload>

      <span class="label-teste">Método</span>
      <v-select
        v-model="method"
        :items="methods"
        item-title="label"
        item-value="value"
        placeholder="Selecione um método"
        variant="outlined"
        density="compact"
        hide-details
        class="my-6 custom-width"
      />

      <v-checkbox class="label-teste" v-model="custom" label="Personalizada" density="compact" hide-details />

      <v-file-upload v-if="custom" 
        v-model="parametros"
        accept=".txt"
        density="compact" 
        variant="compact"
        hide-browse
        divider=""
        :disabled="status === 'reading'"
        class="upload-box"
        @update:model-value="onArquivo"
        >
        <template #icon>
          <span v-if="!parametros" class="upload-icon">
            <v-icon :icon="parametros ? 'mdi-file-document-outline' : 'mdi-tray-arrow-up'" size="22" />
          </span>
        </template>

        <template #title>
          <div v-if="parametros" class="arquivo-info">
            <span class="arquivo-nome">{{ parametros.name }}</span>
            <span class="arquivo-tipo">{{ parametros.type || 'texto' }}</span>
          </div>
          <span v-else class="font-weight-bold">Adicionar parâmetros</span>
        </template>
      </v-file-upload>

      <div class="d-flex justify-space-between text-caption text-medium-emphasis mt-2 mb-6">
        <span class="label-teste">Teste: {{ test }}%</span>
      </div>
      <v-text-field
        v-model="test" 
        type="number"
        min="0" 
        max="99" 
        placeholder="%Teste" 
        variant="outlined" 
        density="compact" 
        class="mt-4 custom-width"
        hide-details 
      />

      <i class="mdi-play"></i>
      <v-btn
        color="purple"
        block
        height="44"
        prepend-icon="mdi-play"
        class="text-none btn-executar"
        :disabled="status === 'reading'"
        @click="executar"
        >
        Executar
      </v-btn>
    

    <p v-if="error" role="alert" class="text-body-2 mt-4">{{ error }}</p>

    </aside>
  </div>
</template>

<style scoped>
.layout {
  color: #fff;
  width: 100%;
  height: 100%;
  padding: 5px;
  font-weight: 700;
}

.label-teste{
  color: #fff;
  font-weight: 700;
  font-size: 13px;
}

.upload-box :deep(.v-file-upload-items),
.upload-box :deep(.v-file-upload-item),
.upload-box :deep(.v-list) {
  display: none !important;
}

.arquivo-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.arquivo-nome {
  font-weight: 700;
  word-break: break-all;
}

.arquivo-tipo {
  font-size: 0.75rem;
  opacity: 0.7;
}

.upload-box :deep(.v-file-upload-dropzone) {
  display: flex !important;
  min-height: 0 !important;
  height: auto !important;
  padding: 14px 12px !important;
  background: transparent !important;
  border: 1px dashed rgba(213, 18, 231, 0.664) !important;
  border-radius: 6px;
  gap: 8px;
  margin-top: 10px;
}

.upload-box :deep(.v-file-upload-icon) {
  margin: 0 !important;
}

.upload-box :deep(.v-file-upload-title) {
  margin: 0 !important;
  font-size: 0.95rem;
  color: #fff;
}

.upload-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: #a813d2;
  color: #ffffff;
}

.upload-icon-parametros{
  color: #ffffff;
}

.custom-width{
  margin-bottom: 10px;
}

.custom-width :deep(.v-field__input) {
  min-height: 56px;
  font-size: 1rem;
}

.btn-executar{
  background-color: #861da2;
  margin-bottom: 10px;
}

.btn-analise{
    color: #861da2;
    font-weight: 700;
}

.layout :deep(.v-btn__prepend) {
  margin-inline-end: 12px;
}
</style>