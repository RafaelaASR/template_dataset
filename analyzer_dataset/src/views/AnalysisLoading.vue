<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

defineProps({
  aba: { type: String, default: 'dataset' },
})

const steps = [
  'Lendo o arquivo',
  'Dividindo treino e teste',
  'Treinando o modelo',
  'Calculando as métricas',
]

const step = ref(0)
let timer = null

onMounted(() => {
  timer = setInterval(() => {
    if (step.value < steps.length - 1) step.value++
    else clearInterval(timer)
  }, 1500)
})

onBeforeUnmount(() => clearInterval(timer))

function estado(i) {
  return i < step.value ? 'complete' : i === step.value ? 'active' : 'pending'
}
const legenda = { complete: 'Concluída', active: 'Em andamento', pending: 'Aguardando' }
</script>

<template>
  <div class="loading-wrap">
    <section class="analysis" aria-label="Progresso da análise">
      <ol class="steps">
        <li v-for="(label, i) in steps" :key="label" :data-state="estado(i)"
            :aria-current="i === step ? 'step' : undefined">
          <v-icon v-if="estado(i) === 'complete'" icon="mdi-check-circle" color="success" size="18" />
          <v-progress-circular v-else-if="estado(i) === 'active'"
                               indeterminate size="16" width="2" color="#861da2" />
          <v-icon v-else icon="mdi-circle-outline" size="18" />
          <div class="d-flex flex-column">
            <span>{{ label }}</span>
            <small>{{ legenda[estado(i)] }}</small>
          </div>
        </li>
      </ol>
    </section>

    <!-- esqueletos -->
    <div class="mt-7" aria-busy="true" aria-hidden="true">
      <div class="metrics mb-8">
        <div v-for="nome in ['Registros', 'Colunas', 'Teste']" :key="nome" class="metric">
          <p class="text-caption text-medium-emphasis">{{ nome }}</p>
          <div class="skeleton sk-valor mt-2" />
        </div>
      </div>

      <div class="skeleton sk-titulo mt-5 mb-5" />

      <div v-if="aba === 'dataset'" class="sk-tabela">
        <div v-for="linha in 6" :key="linha" class="sk-linha">
          <div v-for="coluna in 4" :key="coluna" class="skeleton sk-celula" />
        </div>
      </div>

      <div v-else class="sk-grafico">
        <div v-for="n in 4" :key="n">
          <div class="skeleton sk-rotulo mb-2" />
          <div class="skeleton sk-barra" :style="{ width: 90 - n * 15 + '%' }" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.loading-wrap { width: 100%; padding: 16px; }
.roxo { color: #861da2; }

.track {
  height: 4px; margin: 16px 0 20px;
  background: #ead9f2; border-radius: 3px; overflow: hidden;
}
.track span {
  display: block; height: 100%; width: 36%;
  background: #861da2;
  animation: travel 1.6s ease-in-out infinite;
}

.steps {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 20px;
}

.steps li {
  display: flex;
  flex-wrap: nowrap;
  align-items: center;
  gap: 10px;
  font-size: 0.875rem;
  opacity: 0.6;
  margin-bottom: 10px;
}

.steps li > div {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 8px;
}

.steps li small {
  font-size: 0.7rem;
  opacity: 0.7;
  white-space: nowrap;
}

.steps li[data-state='active'] {
  color: #861da2;
  font-weight: 600;
  opacity: 1;
}

.steps li[data-state='complete'] {
  opacity: 1;
}
.metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.metric { padding: 16px; border: 1px solid rgba(0, 0, 0, 0.12); border-radius: 6px; }

.skeleton {
  border-radius: 4px;
  background: #f1ecf5;
  background-image: linear-gradient(90deg, #f1ecf5 20%, #ead9f2 50%, #f1ecf5 80%);
  background-size: 200% 100%;
  animation: shimmer 1.8s ease-in-out infinite;
}
.sk-valor { height: 28px; width: 60%; }
.sk-titulo { height: 24px; width: 160px; margin-top: 10px; margin-bottom: 10px;}
.sk-tabela { display: grid; gap: 12px; }
.sk-linha { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.sk-celula { height: 12px; }
.sk-grafico { display: grid; gap: 16px; }
.sk-rotulo { height: 12px; width: 96px; }
.sk-barra { height: 16px; }

@keyframes travel { 0% { margin-left: -36%; } 100% { margin-left: 100%; } }
@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

@media (prefers-reduced-motion: reduce) {
  .track span, .skeleton { animation: none; }
  .track span { width: 100%; opacity: 0.65; }
}
</style>