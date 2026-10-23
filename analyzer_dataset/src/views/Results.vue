<script setup>
import { ref, computed, watch } from 'vue'
import AnalysisLoading from './AnalysisLoading.vue'

const props = defineProps({ 
  resultado: Object, 
  isLoading: Boolean,
  methods: Object
})

const aba = ref('dataset')
const page = ref(1)
const porPagina = 50
const linhas = ref([])
const carregandoPagina = ref(false)
const resultadosHistorico = ref([])

const totalPaginas = computed(() =>
  Math.max(1, Math.ceil((props.resultado?.registros ?? 0) / porPagina))
)

const colunasResultado = computed(() => {
  const primeiro = resultadosHistorico.value[0]
  return primeiro ? Object.keys(primeiro) : []
})

const method = ref(null)

watch(
  () => props.resultado?.resultados,
  (novos) => {
    if (!novos) return

    resultadosHistorico.value = [...novos]
  },
  { immediate: true, deep: true }
)

watch(
  [page, () => props.resultado?.dataset_id],
  async ([nova, datasetId]) => {
    if (!datasetId || !props.resultado) return

    carregandoPagina.value = true

    try {
      const offset = (nova - 1) * porPagina

      if (nova === 1) {
        linhas.value = props.resultado.dadosDataset ?? []
        return
      }

      const resp = await fetch(
        `http://localhost:8000/api/dataset/${datasetId}?offset=${offset}&limit=${porPagina}`
      )

      if (!resp.ok) {
        throw new Error((await resp.json()).detail)
      }

      const data = await resp.json()
      linhas.value = data.linhas
    } catch (e) {
      console.error('Erro ao carregar página:', e)
    } finally {
      carregandoPagina.value = false
    }
  },
  { immediate: true }
)
</script>

<template>
  <div class="result-content d-flex flex-column">
     <div v-if="resultado?.registros && isLoading == false" class="metrics px-4 pb-2">
        <div class="metric">
          <p class="text-caption text-medium-emphasis">Registros</p>
          <p class="text-h5 font-weight-bold mt-2">
            {{ resultado?.registros.toLocaleString('pt-BR') }}
          </p>
        </div>
        <div class="metric">
          <p class="text-caption text-medium-emphasis">Colunas</p>
          <p class="text-h5 font-weight-bold mt-2">{{ resultado?.colunas }}</p>
        </div>
        <div class="metric">
          <p class="text-caption text-medium-emphasis">Teste</p>
          <p class="text-h5 font-weight-bold mt-2">{{ Math.round(resultado?.teste * 100) }}%</p>
      </div>
    </div>
    <div v-if="aba == 'resultados'" class="d-flex">
      <v-text-field label="Buscar método" variant="outlined"></v-text-field>
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
    </div>
    <VTabs v-model="aba" color="#861da2" height="36" class="px-4 pb-0 flex-grow-0">
      <VTab value="dataset" text="Dataset" prepend-icon="mdi-database" />
      <VTab value="resultados" text="Resultados" prepend-icon="mdi-text-box-outline" />
    </VTabs>

    <AnalysisLoading v-if="isLoading" :aba="aba" class="flex-grow-1" style="min-height: 0" />
    
    <div v-else-if="isLoading == false && (!props.resultado || props.resultado?.length === 0)"
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

    <VTabsWindow v-else v-model="aba" class="janela">
      <VTabsWindowItem value="dataset" class="item-dataset px-4">
        <div class="nome-dataset">
          <h4 class="text-subtitle-1 font-weight-bold">{{ resultado?.dataset }}</h4>
          <p class="text-caption text-medium-emphasis" style="font-size: 13px;">
            Página {{ page }} de {{ totalPaginas }} ·
            {{ resultado?.registros.toLocaleString('pt-BR') }} registros
          </p>
        </div>
        <div class="area-scroll">
          <div class="tabela-area">
            <v-table v-if="linhas.length" density="compact" class="tabela">
              <thead>
                <tr>
                  <th>#</th>
                  <th v-for="(nome, j) in resultado.colunas_nomes" :key="nome">
                    {{ nome }}
                  </th>
                </tr>
              </thead>
              <tbody :style="{ opacity: carregandoPagina ? 0.5 : 1 }">
                <tr v-for="(linha, i) in linhas" :key="i">
                  <td class="text-medium-emphasis">
                    {{ (page - 1) * porPagina + i + 1 }}
                  </td>
                  <td
                    v-for="(valor, j) in linha"
                    :key="j"
                    :class="{ 'col-alvo': j === resultado.indice_alvo }"
                  >
                    {{ valor }}
                  </td>
                </tr>
              </tbody>
            </v-table>
          </div>
        </div>

        <div class="paginacao text-center">
          <v-pagination
            v-model="page"
            :length="totalPaginas"
            :total-visible="5"
            :disabled="carregandoPagina"
            rounded="circle"
            active-color="#861da2"
          />
        </div>
      </VTabsWindowItem>
        
      <VTabsWindowItem value="resultados" class="pa-4">
        <v-table density="compact" class="border rounded">
          <thead>
            <tr>
              <th v-for="chave in colunasResultado" :key="chave">
                {{ chave }}
              </th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="(r, index) in resultado?.resultados ?? []"
              :key="r.modelo ?? index"
            >
              <td v-for="chave in colunasResultado" :key="chave">
                {{ r[chave] ?? '—' }}
              </td>
            </tr>
          </tbody>
        </v-table>
      </VTabsWindowItem>
    </VTabsWindow>
  </div>
</template>

<style scoped>
.loading{
  position: relative;
  width: 100%;
}

.result-content {
  background-color: #ffffff;
  width: 100%;
  height: 100%;
  min-height: 0;
  overflow: hidden;
  padding: 16px 20px;
}

.result-content :deep(.v-tabs) {
  height: auto !important;
  flex: 0 0 auto;
}

.result-content :deep(.v-tab) {
  min-height: 36px;
  height: 44px;
  margin-bottom: 8px;
  margin-inline-end: 12px;
}

.janela {
  flex: 1 1 0;
  min-height: 0;
}
.janela :deep(.v-window__container),
.janela :deep(.v-window-item) {
  height: 100%;
}

.item-dataset {
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.nome-dataset {
  flex: 0 0 auto;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  text-align: right;
  margin-bottom: 12px;
}

.area-scroll {
  flex: 1 1 0;
  min-height: 0;
  overflow-y: auto;
}

.tabela-area {
  border: 1px solid rgba(0, 0, 0, 0.12);
  border-radius: 6px;
}

.paginacao {
  margin-top: 8px;
  padding-bottom: 8px;
}

.col-alvo {
  background-color: #f4effa;
  font-weight: 600;
  color: #861da2;
}

.painel-resultado {
  height: calc(100vh - 64px);
  min-height: 0;
}

.result-content :deep(.v-tab .v-btn__prepend) {
  margin-inline-end: 12px;
}

.title-icon{
  background-color: #EAD9F2;
  color: #861da2;
  border-radius: 15px;
  padding: 25px;
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

.metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.metric {
  margin-top: 10px;
  padding: 16px;
  border: 1px solid rgba(0, 0, 0, 0.12);
  border-radius: 6px;
}

.nome-dataset{
  margin-bottom: 20px;
}

.paginacao{
  margin-top: 5px;
}
</style>