<template>
  <div class="login">
    <h1 class="login__title">Sign In</h1>

    <div class="login__form">
      
      <form @submit.prevent="handleForm">
        <div class="login__content">
          
          <!-- Email Input -->
          <div class="login__box">
            <i class="login__icon fas fa-envelope"></i>
            <div class="login__box-input">
              <input 
                type="email" 
                id="email" 
                v-model="userInfo.email" 
                class="login__input" 
                :class="{ 'error': validationErrors.email }" 
                required
                @blur="validateEmail"
              />
              <label for="email" class="login__label">Email</label>
            </div>
          </div>
          <p v-if="validationErrors.email" class="login-err">{{ validationErrors.email }}</p>
          <p v-if="error?.email" class="login-err">{{ error.email[0] }}</p>

          <!-- Password Input -->
          <div class="login__box">
            <i class="login__icon fas fa-lock"></i>
            <div class="login__box-input">
              <input 
                :type="showPassword ? 'text' : 'password'" 
                id="password" 
                v-model="userInfo.password" 
                class="login__input" 
                :class="{ 'error': validationErrors.password }" 
                required
                @blur="validatePassword"
              />
              <label for="password" class="login__label">Password</label>
              <i 
                class="login__eye fas" 
                :class="showPassword ? 'fa-eye-slash' : 'fa-eye'" 
                @click="togglePassword"
              ></i>
            </div>
          </div>
          <p v-if="validationErrors.password" class="login-err">{{ validationErrors.password }}</p>
          <p v-if="error?.password" class="login-err">{{ error.password[0] }}</p>
          <p v-if="error?.non_field_errors" class="login-err">{{ error.non_field_errors[0] }}</p>

          <!-- Remember Me & Forgot Password -->
          <div class="login__check">
            <div class="login__check-group">
              <input type="checkbox" id="remember" class="login__check-input">
              <label for="remember" class="login__check-label">Remember me</label>
            </div>
            <a href="#" class="login__forgot">Forgot Password?</a>
          </div>

          <!-- Submit Button -->
          <button class="login__button" type="submit" :disabled="loading">
            <span v-if="loading">
              <i class="fas fa-spinner fa-spin"></i> Signing in...
            </span>
            <span v-else>Sign in</span>
          </button>

          <!-- Register Link -->
          <p class="login__register">
            Don't have an account? <a href="#">Register</a>
          </p>

        </div>
      </form>
    </div>
  </div>
</template>



<style scoped>

:root {
  --white-color: hsl(0, 0%, 100%);
  --black-color: hsl(0, 0%, 0%);
  --body-font: "Poppins", sans-serif;
  --h1-font-size: 1.75rem;
  --normal-font-size: 1rem;
  --small-font-size: 0.813rem;
  --font-medium: 500;
}

* {
  box-sizing: border-box;
  padding: 0;
  margin: 0;
}



body,
input,
button {
  font-size: var(--normal-font-size);
  font-family: var(--body-font);

}

body {
  color: var(--white-color);
  
}

input,
button {
  border: none;
  outline: none;
}

a {
  text-decoration: none;
}

img {
  max-width: 100%;
  height: auto;
}



.login__img {
  position: absolute;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.login__form {
  position: relative;
  padding: 2.5rem 2rem;
  border-radius: 20px;
  background: white;
  width: 380px;
  margin: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(226, 232, 240, 0.7);
}

@keyframes gradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.login__title {
  text-align: center;
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 2rem;
  color: #1a2e44;
}

.login__content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.login__box {
  position: relative;
  display: flex;
  align-items: center;
}

.login__icon {
  position: absolute;
  left: 1rem;
  color: #666;
  font-size: 1.25rem;
}

.login__box-input {
  width: 100%;
}

.login__input {
  width: 100%;
  padding: 1rem 1rem 1rem 3rem;
  border: 1px solid #ddd;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.login__input:focus {
  border-color: #4A90E2;
  outline: none;
}

.login__label {
  position: absolute;
  left: 3rem;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
  transition: all 0.3s;
  pointer-events: none;
  background-color: white;
  padding: 0 0.25rem;
}

.login__input:focus + .login__label,
.login__input:not(:placeholder-shown) + .login__label {
  top: 0;
  transform: translateY(-50%) scale(0.8);
  color: #4A90E2;
}

.login__eye {
  position: absolute;
  right: 1rem;
  color: #666;
  cursor: pointer;
}

.login__check {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 1rem 0;
}

.login__check-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.login__check-input {
  width: 1rem;
  height: 1rem;
}

.login__forgot,
.login__register {
  color: #4A90E2;
  text-decoration: none;
}

.login__forgot:hover,
.login__register:hover {
  text-decoration: underline;
}

.login-err {
  color: #dc3545;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

/* Fade-in Animation */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}


</style>


<script>
import useAxios from '@/composables/fetchCredentials/axios';
import {ref, onMounted, computed, reactive} from 'vue';
import {useRouter} from "vue-router";
export default {
  name: "LoginForm",
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const showPassword = ref(false)
    const validationErrors = reactive({
      email: '',
      password: ''
    })

    const userInfo = reactive({
      email: '',
      password: ''
    })

    const { login, error, isAuthenticatedComputed } = useAxios()

    const validateEmail = () => {
      validationErrors.email = ''
      if (!userInfo.email) {
        validationErrors.email = 'Email is required'
        return false
      }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(userInfo.email)) {
        validationErrors.email = 'Please enter a valid email address'
        return false
      }
      return true
    }

    const validatePassword = () => {
      validationErrors.password = ''
      if (!userInfo.password) {
        validationErrors.password = 'Password is required'
        return false
      }
      if (userInfo.password.length < 6) {
        validationErrors.password = 'Password must be at least 6 characters'
        return false
      }
      return true
    }

    const togglePassword = () => {
      showPassword.value = !showPassword.value
    }

    const handleForm = async () => {
      if (!validateEmail() || !validatePassword()) {
        return
      }

      try {
        loading.value = true
        await login(userInfo)
      } catch (err) {
        console.error('Login error:', err)
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      if (isAuthenticatedComputed.value) {
        router.push({ name: 'home' })
      }
    })

    return {
      userInfo,
      loading,
      error,
      showPassword,
      validationErrors,
      handleForm,
      validateEmail,
      validatePassword,
      togglePassword
    }
  },
}
</script>

