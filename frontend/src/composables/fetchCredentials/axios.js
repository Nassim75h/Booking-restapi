import { jwtDecode } from 'jwt-decode';
import axios from 'axios';
import {useRouter} from "vue-router";
import {ref, computed} from 'vue';

const useAxios = (userInfo) => {
    const router = useRouter();
    const userCredentials = ref(null)
    const responseMessage = ref(null)
    const responseStatus = ref(null)
    const error = ref(null)
    const isAuthenticated = ref(false)
    const API_URL = 'http://localhost:8000';
    
    const getAccessToken = () => localStorage.getItem('access');
    const getRefreshToken = () => localStorage.getItem('refresh');
    
    const currentToken = getAccessToken();
    
    const apiClient = axios.create({
        baseURL: `${API_URL}/api/v0/`,
        headers: {
            'Content-Type': 'application/json'
        },
        timeout: 10000 // 10 second timeout
    });
    
    // Set initial auth header if token exists
    const initialToken = getAccessToken();
    if (initialToken) {
        apiClient.defaults.headers.Authorization = `Bearer ${initialToken}`;
    }
    
    // Add response interceptor for error handling
    apiClient.interceptors.response.use(
        response => response,
        async error => {
            const originalRequest = error.config;
            
            // Check if error is due to token expiration
            if (error.response?.status === 401 && !originalRequest._retry) {
                originalRequest._retry = true;
                const refresh = getRefreshToken();
                
                if (refresh) {
                    try {
                        // Try to get a new access token
                        const response = await axios.post(`${API_URL}/api/v0/auth/token/refresh/`, {
                            refresh: refresh
                        });
                        
                        if (response.data.access) {
                            localStorage.setItem('access', response.data.access);
                            apiClient.defaults.headers['Authorization'] = `Bearer ${response.data.access}`;
                            originalRequest.headers['Authorization'] = `Bearer ${response.data.access}`;
                            return apiClient(originalRequest);
                        }
                    } catch (refreshError) {
                        console.error('Token refresh failed:', refreshError);
                        localStorage.removeItem('access');
                        localStorage.removeItem('refresh');
                        isAuthenticated.value = false;
                        router.push('/login');
                        return Promise.reject(refreshError);
                    }
                } else {
                    isAuthenticated.value = false;
                    router.push('/login');
                }
            }
            return Promise.reject(error);
        }
    );

    // Add request interceptor for error handling
    apiClient.interceptors.request.use(
        config => {
            // Always get the latest token
            const currentToken = localStorage.getItem('access');
            if (currentToken) {
                config.headers.Authorization = `Bearer ${currentToken}`;
            }
            return config;
        },
        error => {
            return Promise.reject(error);
        }
    );
    
    const checkAuthenticationStatus = async () => {
        const token = getAccessToken();
        if (token) {
            try {
                // Verify token by fetching user details
                const response = await apiClient.get('auth/profile/');
                userCredentials.value = response.data;
                apiClient.defaults.headers.Authorization = `Bearer ${token}`;
                isAuthenticated.value = true;
            } catch (err) {
                console.error('Token validation failed:', err);
                userCredentials.value = null;
                delete apiClient.defaults.headers.Authorization;
                isAuthenticated.value = false;
                localStorage.removeItem('access');
                localStorage.removeItem('refresh');
            }
        } else {
            userCredentials.value = null;
            delete apiClient.defaults.headers.Authorization;
            isAuthenticated.value = false;
        }
    };

    // Check auth status on initialization
    checkAuthenticationStatus();
    
    const login = async (credentials) => {
        try {
            const response = await axios.post(`${API_URL}/api/v0/auth/login/`, 
                {
                    email: credentials?.email,
                    password: credentials?.password,
                },
                {
                    headers: {
                        "Content-Type": "application/json",
                    }
                }
            );
            const {access, refresh} =  response.data;
            localStorage.setItem("access", access);
            localStorage.setItem("refresh", refresh);
            
            // Update axios instance headers and auth status
            apiClient.defaults.headers.Authorization = `Bearer ${access}`;
            isAuthenticated.value = true;
            router.push({ name: "home" });
        } catch (err) {
            error.value = err.response?.data;
            console.error('Login error:', err.response?.data);
            isAuthenticated.value = false;
        }
    };

    const logout = () => {
        localStorage.removeItem('access');
        localStorage.removeItem('refresh');
        delete apiClient.defaults.headers.Authorization;
        isAuthenticated.value = false;
        router.push('/login');
    };
    
    const activateAccount = async(activationToken) => {
        try {
            const response = await axios.get(`${API_URL}/activate/${activationToken.value}/`);
            
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
            console.log('Sending registration request with data:', {
                email: userInfo.email,
                username: userInfo.userName,
                first_name: userInfo.firstName,
                last_name: userInfo.lastName,
                terms_cond: userInfo.terms
            });

            const response = await axios.post(`${API_URL}/api/v0/auth/register/`, {
                email: userInfo.email,
                username: userInfo.userName,
                first_name: userInfo.firstName,
                last_name: userInfo.lastName,
                password: userInfo.password,
                confirm_password: userInfo.confirmPassword,
                terms_cond: userInfo.terms,
            }, {
                headers: {
                    "Content-Type": "application/json",
                }
            });

            console.log('Registration response:', response.data);

            if (response.status === 201 || response.status === 200) {
                responseMessage.value = "Registration successful! Redirecting to login...";
                setTimeout(() => {
                    router.push({name: "login"});
                }, 1500);
            }
        } catch(err) {
            console.error('Registration error:', {
                status: err.response?.status,
                statusText: err.response?.statusText,
                data: err.response?.data,
                message: err.message,
                url: err.config?.url
            });
            
            if (err.response?.data?.detail) {
                responseMessage.value = err.response.data.detail;
            } else if (err.response?.data?.message) {
                responseMessage.value = err.response.data.message;
            } else if (err.response?.status === 400) {
                // Handle validation errors
                const errors = err.response?.data;
                if (typeof errors === 'object') {
                    const firstError = Object.values(errors)[0];
                    responseMessage.value = Array.isArray(firstError) ? firstError[0] : firstError;
                } else {
                    responseMessage.value = "Please check your input data.";
                }
            } else if (err.response?.status === 404) {
                responseMessage.value = "Registration service is currently unavailable.";
            } else if (!err.response) {
                responseMessage.value = "Cannot connect to the server. Please try again later.";
            } else {
                responseMessage.value = "Registration failed. Please try again later.";
            }
        }
    }
    
    const fetchUserDetails = async () => {
        try {
            const token = getAccessToken();
            if (!token) {
                userCredentials.value = null;
                isAuthenticated.value = false;
                return null;
            }
            const response = await apiClient.get('auth/profile/');
            userCredentials.value = response.data;
            isAuthenticated.value = true;
            return response.data;
        } catch (err) {
            console.error('Error fetching user details:', err);
            userCredentials.value = null;
            isAuthenticated.value = false;
            if (err.response?.status === 401) {
                // Clear invalid tokens
                localStorage.removeItem('access');
                localStorage.removeItem('refresh');
            }
            if (err.response?.status === 401) {
                // Token is invalid, clear it
                logout();
            }
            return null;
        }
    };

    const get = (url, config = {}) => apiClient.get(url, config);
    const post = (url, data, config = {}) => apiClient.post(url, data, config);
    const put = (url, data, config = {}) => apiClient.put(url, data, config);
    const del = (url, config = {}) => apiClient.delete(url, config);
    const isAuthenticatedComputed = computed(() => {
        return isAuthenticated.value && !!userCredentials.value;
    });

    // Recheck auth status when window gains focus
    if (typeof window !== 'undefined') {
        window.addEventListener('focus', () => {
            checkAuthenticationStatus();
        });
    }
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
