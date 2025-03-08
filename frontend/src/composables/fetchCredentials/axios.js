import { jwtDecode } from 'jwt-decode';
import axios from 'axios';
import {useRouter} from "vue-router";
import {ref, computed, reactive} from 'vue';


    const useAxios = (userInfo) => {
    const router = useRouter();
    const userCredentials =ref(null)
    const responseMessage =ref(null)
    const responseStatus = ref(null)
    const error = ref()
    const isAuthenticated = ref(false)
    const accessToken = localStorage.getItem("access") ;
    const refreshToken = localStorage.getItem("refresh") ;
    const apiClient = axios.create({
        baseURL: 'http://localhost:8000/api/v0/',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': accessToken? `Bearer ${accessToken}` : "",
        }
    });
    const checkAuthenticationStatus = () => {
        if (accessToken) {
            isAuthenticated.value = true;
        } else {
            isAuthenticated.value = false;
        }
    };
    checkAuthenticationStatus();
    
    apiClient.interceptors.response.use((response) => response,
        async (error) => {
        
        if (error.response && error.response.status === 401 && refreshToken) {
            try {
                const response = await axios.post("http://localhost:8000/api/v0/auth/token/refresh/",{
                    refresh : refreshToken,
                })
                const newAccessToken = response.data.access;
                const newRefreshToken = response.data.refresh;
                if (newRefreshToken) {
                    localStorage.setItem("refresh",newRefreshToken)
                }
                localStorage.setItem("access", newAccessToken)
                apiClient.defaults.headers.Authorization = `Bearer ${newAccessToken}`;
                error.config.headers.Authorization = `Bearer ${newAccessToken}`
                isAuthenticated.value = true
              
                return apiClient(error.config)
            }catch(err) {
                console.log("Token  refresh failed :",err)
                localStorage.removeItem("access")
                localStorage.removeItem("refresh")
                isAuthenticated.value = false
                await logout()
                router.push({ name: "login" })
                
                return Promise.reject(err)
         
            }
        }
        return Promise.reject(error);

        });
    
    const login = async () => {
        try {
            const response = await axios.post('http://localhost:8000/api/v0/auth/login/', {
                headers: {
                    "Content-Type": "application/json",
                },
                    email: userInfo?.email,
                    password: userInfo?.password,
                })
            const {access, refresh} =  response.data
            localStorage.setItem("access", access)
            localStorage.setItem("refresh", refresh)
            router.push({ name: "home" })
        } catch (err) {
            error.value = err.response.data;
            console.log(err.response.data);
        }
    };

    const logout = () => {
        const confirmLogout = window.confirm("Are you sure you want to log out?");
        
        if (confirmLogout) {
            localStorage.removeItem("access");
            localStorage.removeItem("refresh");
            router.push({ name: "login" });
        }
    };
    
    const activateAccount = async(activationToken) => {
        try {
            const response = await axios.get("http://localhost:8000/activate/"+activationToken.value+'/');
            
            if(response.status==200){
                const {data} = response;
                localStorage.setItem("access",data.access)
                localStorage.setItem("refresh",data.refresh)
                setTimeout(() =>{
                      router.push({ name: "home" })
                  }
                  ,3000)
                responseMessage.value=data.message;
            }
            
        
        }catch(err) {
            console.log(err);
            if(err.status===403) {
                setTimeout(() => {
                      router.push({name: "login"})
                  }
                  , 3000)
                responseMessage.value =err.response.data.message
            }
        }
    
    }
    const registerUser = async() => {
        try {
            
            // console.log(userInfo)
            const response = await axios.post("http://localhost:8000/api/v0/auth/register/", {
                headers: {
                    "Content-Type": "application/json",
                },
                email: userInfo.email,
                username: userInfo.userName,
                first_name: userInfo.firstName,
                last_name: userInfo.lastName,
                password: userInfo.password,
                confirm_password: userInfo.confirmPassword,
                terms_cond: userInfo.terms,
            })
            login()
        }catch(err) {
            console.log(err)
        }
    }
    
    
    const fetchUserDetails = async() => {
        try{
            const response = await apiClient.get("http://localhost:8000/api/v0/auth/profile/");
            const {data} =  response;
            userCredentials.value = data
        }catch(err) {
            console.log(err.message)
        }
        
    }

    const get = (url, config = {}) => apiClient.get(url, config);
    const post = (url, data, config = {}) => apiClient.post(url, data, config);
    const put = (url, data, config = {}) => apiClient.put(url, data, config);
    const del = (url, config = {}) => apiClient.delete(url, config);
    const isAuthenticatedComputed = computed(() => isAuthenticated.value);
    
    return {
        error,
        fetchUserDetails,
        logout,
        isAuthenticatedComputed,
        responseMessage,
        userCredentials,
        responseStatus,
        activateAccount,
        registerUser,
        login,
        get,
        post,
        put,
        del,
        
    }
}
export default useAxios;
