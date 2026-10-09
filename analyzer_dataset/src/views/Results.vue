<script setup>
import { ref } from 'vue'

defineProps({
  run: { type: Object, default: null },
  dataset: { type: Object, default: null },
})
defineEmits(['selecionar-arquivo'])

const aba = ref('dataset')
</script>

<template>
  <div class="result-content d-flex flex-column">
    <header class="d-flex align-center justify-space-between ga-4 px-4">
      <div class="d-flex align-center ga-4">
          <v-icon class="title-icon" :icon="aba === 'dataset' ? 'mdi-table' : 'mdi-text-box-outline'" size="23" />
          <h2 class="text-subtitle-1 font-weight-bold">
            {{ aba === 'dataset' ? 'Visão geral' : 'Distribuição dos dados' }}
          </h2>
      </div>
      <span class="text-caption text-medium-emphasis d-flex align-center ga-1">
        <v-icon icon="mdi-circle" size="8" color="grey" />
        {{ run ? 'Concluído' : 'Nenhuma análise' }}
      </span>
    </header>
    <VTabs v-model="aba"  color="#861da2" height="36" class="px-4 pt-4 pb-0 flex-grow-0">
      <VTab value="dataset" text="Dataset" prepend-icon="mdi-database" />
      <VTab value="resultados" text="Resultados" prepend-icon="mdi-text-box-outline" />
    </VTabs>

    

    <div v-if="!run || !dataset"
      class="empty-area d-flex flex-column align-center text-center flex-grow-1 py-12"
    >
      <div class="empty-illustration" aria-hidden="true">
        <div class="file-illustration">
          <v-icon icon="mdi-table" size="23" />
          <div class="illustration-line" />
          <div class="illustration-line" />
          <div class="illustration-line w-66" />
        </div>
        <div class="illustration-chart">
          <v-icon icon="mdi-text-box-outline" size="34" />
        </div>
        <v-icon icon="mdi-plus" size="16" color="primary" class="plus plus-a" />
        <v-icon icon="mdi-plus" size="11" color="primary" class="plus plus-b" />
      </div>

      <h3 class="text-h6 font-weight-bold empty-text">Nenhum dataset informado</h3>
      <p class="text-body-2 text-medium-emphasis mt-3 texto-vazio">
        Ainda não há {{ aba === 'dataset' ? 'dataset' : 'resultados' }} para exibir.<br />
        Insira um arquivo e selecione um método para iniciar a análise.
      </p>
    </div>

    <VTabsWindow v-else v-model="aba" class="flex-grow-1 mt-7">
      <VTabsWindowItem value="dataset" class="pa-4">
        <p>Dataset</p>
        <VTable />
      </VTabsWindowItem>

      <VTabsWindowItem value="resultados" class="pa-4">
        <p>Resultados</p>
      </VTabsWindowItem>
    </VTabsWindow>
  </div>
</template>

<style scoped>
.result-content {
  background-color: #ffffff;
  width: 100%;
  height: 100%;
  padding: 20px;
  padding-top: 30px;;
}

.result-content :deep(.v-tabs) {
  height: auto !important;
  flex: 0 0 auto;
}

.result-content :deep(.v-tab) {
  min-height: 36px;
  height: 50px;
  margin-bottom: 20px;
}

.result-content :deep(.v-tab .v-btn__prepend) {
  margin-inline-end: 12px;
}

.title-icon{
  background-color: #EAD9F2;
  color: #861da2;
  border-radius: 15px;
  padding: 30px;
}

.empty-text{
    margin-top: 40px;
}

.texto-vazio {
  max-width: 310px;
  line-height: 1.5;
}

.empty-area{
  position: relative;
  top: 60px;
}

.empty-illustration {
  position: relative;
  width: 180px;
  height: 130px;
}

.file-illustration {
  position: absolute;
  left: 20px;
  top: 8px;
  width: 90px;
  height: 110px;
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-start;
  background: #f4effa;
  border: 1px solid rgba(134, 29, 162, 0.2);
  border-radius: 10px;
  transform: rotate(-12deg);
  transform-origin: center;
  color: #861da2;

}

.illustration-line {
  height: 6px;
  width: 100%;
  border-radius: 3px;
  background: rgba(134, 29, 162, 0.18);
}

.w-66 {
  width: 66%;
}

.illustration-chart {
  position: absolute;
  right: 30px;
  bottom: -15px;
  width: 70px;
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  color: #861da2;
  background: #ead9f2;
  transform: rotate(10deg);
  transform-origin: center;
}

.plus {
  position: absolute;
  opacity: 0.4;
}
.plus-a { left: 20px; bottom: 20px; }
.plus-b { right: 16px; top: 12px; }

.result-content  :deep(.v-tab) {
  margin-inline-end: 12px;
}
</style>