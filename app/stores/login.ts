import { login } from "~/services/api/login"

export const useLogin = defineStore('login', {
    state: () => ({
        user: null,
    }),
    actions: {
        async enviarLogin(mail: String, password: String) {
            console.log('enviando')
            await login(mail, password)
        }
    }
    
})