<script setup>
import { ref } from 'vue'
import Input from './Input.vue'
import Results from './Results.vue'

const methods = ref([])
const resultado = ref(null)
const isLoading = ref(false)
</script>

<template>
  <div class="d-flex">
    <div>
      <Input
        @update:methods="methods = $event"
        @update:result="resultado = $event"
        @update:loading="isLoading = $event"
      />
    </div>

    <div>
      <Results
        :resultado="resultado"
        :is-loading="isLoading"
        :methods="methods"
        @historico-limpo="resultado && (resultado.resultados = [])"
      />
    </div>
  </div>
</template>