<template>
  <h2>Register</h2>
  <div class="form-signup">
    <div v-if="responseMessage" :class="['message', responseMessage.includes('successful') ? 'success' : 'error']">
      {{ responseMessage }}
    </div>
    <form action=""  >
      <label for="username">Username</label>
      <input v-model="userInfo.userName" placeholder="Username" type="text">
      <label for="first-name">First Name</label>
      <input  v-model="userInfo.firstName" placeholder="First Name" type="text">
      <label for="last-name">Last Name</label>
      <input v-model="userInfo.lastName" type="text" placeholder="Last Name" >
      <label for="email" >Email :</label>
      <input v-model="userInfo.email" type="text" placeholder="Email" >
      <label for="password" >Password :</label>
      <input v-model="userInfo.password" type="password" placeholder="Password" >
      <label  for="confirm-password">Confirm Password</label>
      <input v-model="userInfo.confirmPassword" type="password" placeholder="Confirm Password" >
      <label for="terms"><span><input v-model="userInfo.terms" type="checkbox"> terms and condition</span></label>
      <button class='btn-signup' @click="register"  >Sign up</button>
    </form>
  </div>
</template>

<script>
import   useAxios  from "@/composables/fetchCredentials/axios"
import {ref,reactive} from "vue";

export default {
  name: 'RegisterForm',
  props: {},
  components: [],
  setup(props) {
    const userInfo = reactive({
      email: '',
      password: '',
      firstName: '',
      userName: '',
      lastName: '',
      terms: false,
      confirmPassword: ''
    })
    const {registerUser, responseMessage} = useAxios(userInfo)
    
    const register = async (event) => {
      event.preventDefault()
      
      // Basic validation
      if (!userInfo.email || !userInfo.password || !userInfo.userName || 
          !userInfo.firstName || !userInfo.lastName || !userInfo.confirmPassword) {
        responseMessage.value = "Please fill in all fields"
        return
      }
      
      if (userInfo.password !== userInfo.confirmPassword) {
        responseMessage.value = "Passwords do not match"
        return
      }
      
      if (!userInfo.terms) {
        responseMessage.value = "Please accept the terms and conditions"
        return
      }
      
      await registerUser()
    }
    return {
      userInfo,
      register,
      responseMessage
    }
  }
}
</script>

<style scoped>
:root {
  --white-color: hsl(0, 0%, 100%);
  --black-color: hsl(0, 0%, 0%);
  --primary-color: hsl(205, 100%, 84%);
  --body-font: "Poppins", sans-serif;
  --h1-font-size: 2rem;
  --normal-font-size: 1rem;
  --small-font-size: 0.813rem;
  --font-medium: 500;
}

* {
  box-sizing: border-box;
  padding: 0;
  margin: 0;
}

body {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
}

/* FORM CONTAINER */
.form-signup {
  background-color: white;
  padding: 2.5rem 2rem;
  border-radius: 20px;
  width: 380px;
  text-align: center;
  animation: fadeIn 1s ease-out;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(226, 232, 240, 0.7);
}

@keyframes gradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

/* TITLE */
h2 {
  color: #1a2e44;
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 2rem;
  letter-spacing: -0.5px;
  animation: fadeIn 0.8s ease-out forwards;
}

/* CENTER FORM */
form {
  display: flex;
  flex-direction: column;
  row-gap: 1.2rem;
  width: 100%;
  align-items: center; /* Center items horizontally */
  text-align: center;
}

/* INPUT & LABEL STYLING */
label {
  color: #4b5563;
  font-weight: 500;
  font-size: 0.9rem;
  text-align: left;
  display: block;
  margin-bottom: 0.5rem;
  animation: fadeIn 1s ease-out forwards 0.2s;
}

input {
  width: 100%;
  padding: 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 14px;
  background: #f8fafc;
  color: #1a2e44;
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

input:hover {
  background-color: white;
  border-color: #cbd5e1;
}

input:focus {
  border-color: #4A90E2;
  box-shadow: 0 0 0 4px rgba(74, 144, 226, 0.1);
  outline: none;
}

input::placeholder {
  color: rgba(26, 46, 68, 0.5);
}

/* INPUT FOCUS EFFECT */
input:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0px 0px 8px var(--primary-color);
}

/* CHECKBOX STYLE */
label span {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: var(--small-font-size);
}

input[type="checkbox"] {
  width: 20px;
  height: 20px;
  cursor: pointer;
  border: 2px solid #cbd5e1;
  border-radius: 6px;
  appearance: none;
  position: relative;
  transition: all 0.3s ease;
  background: #f8fafc;
}

input[type="checkbox"]:hover {
  border-color: #6366f1;
  background: white;
}

input[type="checkbox"]:checked {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border: none;
}

input[type="checkbox"]:checked {
  background-color: var(--white-color);
}

input[type="checkbox"]:checked::after {
  content: '✔';
  font-size: 0.9rem;
  color: white;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* SIGN-UP BUTTON */
.btn-signup {
  width: 100%;
  padding: 1rem;
  margin-top: 2rem;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: #fff;
  font-weight: 600;
  cursor: pointer;
  border: none;
  border-radius: 14px;
  transition: all 0.4s ease;
  font-size: 1rem;
  letter-spacing: 0.3px;
  background-size: 200% 200%;
}

.btn-signup:hover {
  background-size: 200% 200%;
  animation: gradient 3s ease infinite;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
}

/* FADE-IN ANIMATION */
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

/* RESPONSIVE */
@media screen and (min-width: 576px) {
  .form-signup {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    justify-content: center;
  }

  h2 {
    font-size: 2.2rem;
  }
}
.message {
  padding: 10px;
  margin-bottom: 15px;
  border-radius: 4px;
  text-align: center;
}

.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}
</style>
