<template>
  <div class="login">
    <img src="your-image.jpg" alt="Background Image" class="login__img">
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
  border: 2px solid var(--white-color);
  padding: 2.5rem 1.5rem;
  border-radius: 1rem;
  backdrop-filter: blur(8px);
  width: 360px;
  margin: auto;
  
}

.login__title {
  text-align: center;
  font-size: var(--h1-font-size);
  font-weight: var(--h1-font-size);
  margin-bottom: 10rem;
  color: rgba(182, 161, 42, 0.987);
}

.login__content {
  display: grid;
  row-gap: 1.75rem;
  margin-bottom: 1.5rem;
}

.login__box {
  display: grid;
  grid-template-columns: max-content 1fr;
  align-items: center;
  column-gap: 0.75rem;
  border-bottom: 2px solid var(--white-color);
}

.login__icon,
.login__eye {
  font-size: 1.25rem;
}

.login__input {
  width: 100%;
  padding: 1rem;
  border: 2px solid var(--white-color);
  background: none;
  color: var(--white-color);
  transition: border 0.4s;
}

.login__input.error {
  border-color: #dc2626;
}

.login-err {
  color: #dc2626;
  font-size: 0.875rem;
  margin-top: 0.25rem;
  margin-bottom: 0.5rem;
}

.login__box-input {
  position: relative;
}

.login__label {
  position: absolute;
  left: 0;
  top: 13px;
  font-weight: var(--font-medium);
  transition: top 0.3s, font-size 0.3s;
}

.login__eye {
  position: absolute;
  right: 0;
  top: 18px;
  z-index: 10;
  cursor: pointer;
}

.login__check {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  transition: all 0.3s ease-in-out;
}

/* Checkbox Animation */
.login__check-input {
  width: 18px;
  height: 18px;
  appearance: none;
  background-color: transparent;
  border: 2px solid var(--white-color);
  border-radius: 4px;
  cursor: pointer;
  position: relative;
  transition: all 0.3s ease-in-out;
}

.login__check-input:checked {
  background-color: var(--white-color);
}

.login__check-input:checked::after {
  content: '✔';
  font-size: 0.9rem;
  color: var(--black-color);
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

/* Label & Link Styling */
.login__check-label,
.login__forgot,
.login__register {
  font-size: var(--small-font-size);
  transition: color 0.3s ease-in-out;
}

.login__forgot,
.login__register a {
  color: var(--white-color);
  text-decoration: none;
  font-weight: bold;
  position: relative;
}

.login__forgot:hover,
.login__register a:hover {
  color: #ffdd57;
  text-decoration: underline;
}

/* Adding a subtle hover effect */
.login__check:hover {
  transform: scale(1.05);
}


.login__forgot {
  color: var(--white-color);
}

.login__forgot:hover,
.login__register a:hover {
  text-decoration: underline;
}

.login__button {
  width: 100%;
  padding: 1rem;
  margin-bottom: 1rem;
  background-color: var(--white-color);
  color: var(--black-color);
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: opacity 0.3s;
}

.login__button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.login__register {
  text-align: center;
}

.login__register a {
  color: var(--white-color);
  font-weight: var(--font-medium);
}

/* Floating Labels */
.login__input:focus + .login__label,
.login__input:not(:placeholder-shown):not(:focus) + .login__label {
  top: -12px;
  font-size: var(--small-font-size);
}

/* Responsive Design */
@media screen and (min-width: 576px) {
  .login__form {
    width: 432px;
    padding: 4rem 3rem 3.5rem;
    border-radius: 1.5rem;
    backdrop-filter: blur(10px);
    animation: fadeIn 1s ease-out;
    display: flex;
    border: 2px solid var(--white-color);
    

  }

  .login__title {
    font-size: 2rem;
  }
}
.login__title {
  text-align: center;
  font-size: var(--h1-font-size);
  font-weight: bold; /* Bold title */
  margin-bottom: 2rem;
  opacity: 0;
  transform: translateY(-20px);
  animation: fadeIn 0.8s ease-out forwards;
}

.login__label {
  position: absolute;
  left: 0;
  top: 13px;
  font-weight: bold; /* Bold label */
  transition: top 0.3s, font-size 0.3s, color 0.3s;
  opacity: 0;
  animation: fadeIn 1s ease-out forwards 0.2s;
}

.login__button {
  color: rgba(12, 14, 29, 0.807);
  width: 100%;
  padding: 1rem;
  border-radius: 0.5rem;
  font-weight: bold; /* Bold button */
  cursor: pointer;
  margin-bottom: 2rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  opacity: 0;
  animation: fadeIn 1s ease-out forwards 0.4s;
}

.login__button:hover {
  transform: scale(1.05);
  box-shadow: 0px 4px 10px rgba(255, 255, 255, 0.3);
}

/* Floating Labels Animation */
.login__input:focus + .login__label,
.login__input:not(:placeholder-shown):not(:focus) + .login__label {
  top: -12px;
  font-size: var(--small-font-size);
  color: var(--white-color);
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

