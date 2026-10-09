import axios from 'axios'

const http = axios.create({ baseURL: import.meta.env.VITE_API_URL })

export async function executar() {
  const { data } = await http.post('/api/executar')
  return data
}