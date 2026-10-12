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