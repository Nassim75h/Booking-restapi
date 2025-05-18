<template>
    <NavBar></NavBar>
    <div class="login-form">
        <LoginForm></LoginForm>
    </div>
</template>

<script>
import NavBar from '@/components/Snippets/NavBar.vue';
import LoginForm from '@/components/Auth/LoginForm.vue';
export default {
    name : "DetailView",
    components :{NavBar,LoginForm},
    props : [],
    setup (props){
        
    return {}
    },

}
</script>

<style>
.login-form {
    margin : 20px 10px ;
}
</style>