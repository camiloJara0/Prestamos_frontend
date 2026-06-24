import axios from 'axios';

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
    
    // Guardar token en localStorage
    localStorage.setItem('token', response.data.token);
    router.push('/Home')

    return response.data;
  } catch (error) {
    console.error('Error en login:', error);
    throw error;
  }
}