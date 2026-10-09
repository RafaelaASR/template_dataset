<script setup>
/*import { executarAnalise } from '@/api'

async function executar() {
    const resposta = await executarAnalise()
    console.log(resposta.mensagem)
}*/
</script>

<template>
  <div class="layout">
    <aside class="sidebar d-flex flex-column ga-4">
        <div class="d-flex align-center ga-2 text-body-2 font-weight-bold">
            <v-icon icon="mdi-tune" size="16" /><span>Configuração</span>
        </div>

        <v-file-upload
            v-model="arquivo"
            accept=".csv,.json"
            hide-browse
            divider=""
            :disabled="status === 'reading'"
            class="upload-box"
            @update:model-value="onArquivo"
            >
            <template #icon>
                <span class="upload-icon">
                <v-progress-circular v-if="status === 'reading'" indeterminate size="20" />
                <v-icon v-else :icon="dataset ? 'mdi-file-delimited-outline' : 'mdi-tray-arrow-up'" size="22" />
                </span>
            </template>

            <template #title>
                <span class="font-weight-bold">{{ dataset ? 'Trocar arquivo' : 'Abrir arquivo' }}</span>
            </template>
        </v-file-upload>

        <span>Método</span>
        <v-select
            v-model="method"
            :items="methods"
            placeholder="Selecione um método"
            variant="outlined"
            density="compact"
            hide-details
            class="my-6 custom-width"
        />

        <v-checkbox v-model="custom" label="Personalizada" density="compact" hide-details />

        <v-select v-if="custom" 
            v-model="target" 
            :items="dataset?.columns ?? []"
            :disabled="!dataset" 
            label="Coluna alvo" 
            placeholder="Selecione uma coluna"
            variant="outlined" 
            density="compact"
            class="mt-4 custom-width" 
        />

        <v-text-field
            v-model.number="test" 
            type="number"
            min="0" 
            max="99" 
            placeholder="%Teste" 
            variant="outlined" 
            density="compact" 
            class="mt-4 custom-width"
            hide-details 
        />
        <div class="d-flex justify-space-between text-caption text-medium-emphasis mt-2 mb-6">
            <span class="label-teste">Teste: {{ Number.isFinite(test) ? test : '' }}%</span>
        </div>

        <i class="mdi-play"></i>
        <v-btn
            color="purple"
            block
            height="44"
            prepend-icon="mdi-play"
            class="text-none btn-executar"
            :disabled="status === 'reading'"
            @click="execute"
            >
            Executar
        </v-btn>
        <v-btn block 
            height="44" 
            prepend-icon="mdi-compare-horizontal"
            class="text-none mt-4 btn-analise"  
            @click="comparison = true">
        Análise comparativa
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
    padding: 20px;
    font-weight: 700;
}

.label-teste{
    color: #fff;
    font-weight: 700;
}

.upload-box :deep(.v-file-upload-dropzone) {
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

.custom-width :deep(.v-field__input) {
  min-height: 56px;
  padding-top: 16px;
  padding-bottom: 16px;
  font-size: 1rem;
}

.btn-executar{
    background-color: #861da2;
}

.btn-analise{
    color: #861da2;
    font-weight: 700;
}

.layout :deep(.v-btn__prepend) {
  margin-inline-end: 12px;
}
</style>