import axios from 'axios';
import api from '~/services/api'

export async function login(email: String, password: String) {
    const config = useRuntimeConfig()
    const router = useRouter()
  try {
    const response = await axios.post(config.public.api + '/' + config.public.login, {
      email,
      password
    },{
    withCredentials: true
  });
    console.log(response.data)
    // Guardar token en localStorage
    localStorage.setItem('token', response.data.access_token);
    router.push('/Home')

    return response.data;
  } catch (error) {
    console.error('Error en login:', error);
    throw error;
  }
}