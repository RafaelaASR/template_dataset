<script setup>
import { ref } from 'vue'
import Input from './Input.vue'
import Results from './Results.vue'

const resultado = ref(null)
const isLoading = ref(false)

const emits = defineEmits(['update:result', 'update:loading'])

</script>

<template>
    <div class="analyzer-content d-flex w-100 ga-0 pa-0">
        <div class="painel-input">
            <Input
                @update:result="resultado = $event"
                @update:loading="isLoading = $event"
            />
        </div>

        <div class="painel-results">
           <Results
                :resultado="resultado"
                :is-loading="isLoading"
                @update:loading="isLoading = $event"
            />
        </div>
    </div>
</template>

<style scoped>
.analyzer-content {
    height: 100vh;
    align-items: stretch;
    overflow: hidden;
}

.painel-input {
    flex: 0 0 23%;
    min-width: 20px;
    padding: 20px;
}

.painel-results {
    flex: 1;
    min-width: 0;
}
</style>