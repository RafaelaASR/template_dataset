<script setup>
import { ref } from 'vue'

const aba = ref('dataset')
</script>

<template>
    <div class="result-content d-flex flex-column">
        <VTabs v-model="aba">
            <VTab value="dataset" text="Dataset" prepend-icon="mdi-database" />
            <VTab value="resultados" text="Resultados" prepend-icon="mdi-chart-line" />
        </VTabs>

        <VTabsWindow v-model="aba" class="flex-grow-1">
            <VTabsWindowItem value="metricas" class="pa-4">
                <p>Resultados</p>
                <VTable />
            </VTabsWindowItem>

            <VTabsWindowItem value="graficos" class="pa-4">
                <p>Gráficos</p>
            </VTabsWindowItem>
        </VTabsWindow>
    </div>
</template>

<style scoped>
.result-content {
    background-color: #ffffff;
    width: 100%;
    height: 100%;
}
</style>