import axios from 'axios'

const http = axios.create({ baseURL: import.meta.env.VITE_API_URL })

export async function executarAnalise(arquivo, metodo, parametros, teste) {
  console.log('executarAnalise', arquivo, metodo, parametros, teste)
  const form = new FormData()
  form.append('arquivo', arquivo)
  form.append('metodo', metodo)
  form.append('teste', teste)
  if (parametros) form.append('parametros', parametros)

  const { data } = await http.post('/api/executar', form)

  console.log("data", data)
  return data
}

export async function buscarHistorico() {
  const { data } = await http.get('/api/historico')
  return data.resultados
}

export async function limparHistorico() {
  const { data } = await http.delete('/api/historico')
  return data.resultados
}