<script setup>

async function executar() {
  const resposta = await executar()
  console.log(resposta.mensagem)
}
</script>
<template>
    <div class="input-content d-flex flex-column">
        <v-file-upload clearable 
            icon=""
            title="Abrir arquivo"
            density="compact" variant="compact">
        </v-file-upload>
        <p>Método</p>
        <VSelect/>
        <v-checkbox label="Personalizada"></v-checkbox>
        <p>% Teste</p>
        <v-number-input
            :reverse="false"
            controlVariant="stacked"
            label=""
            :hideInput="false"
            inset
            :min="0"
            variant="outlined"
        ></v-number-input>
        <VBtn color="purple">
            Executar
        </VBtn>
        <VBtn>
            Análise comparativa
        </VBtn>
    </div>
</template>
<style scoped>
.input-content{
    color: #fff;
    width: 100%;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-top: 20%;
}

</style>
