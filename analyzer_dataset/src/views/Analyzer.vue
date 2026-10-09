<script setup>
import Input from './Input.vue'
import Results from './Results.vue'
</script>

<template>
    <div class="analyzer-content d-flex w-100 ga-0 pa-0">
        <div class="painel-input">
            <Input />
        </div>

        <div class="painel-results">
           <Results
            :run="run"
            :dataset="dataset"
            @selecionar-arquivo="input?.click()"
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
    flex: 0 0 30%;
    min-width: 280px;
    padding: 20px;   /* o respiro fica só no lado do Input */
}

.painel-results {
    flex: 1;
    min-width: 0;
}
</style>