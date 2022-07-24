<template>
  <div>
    <base-title>Login</base-title>
    <login-form :result-is-ready="resultIsReady" @on-login="onLogin" />
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useAuthStore } from "../store__auth";
import { router } from "../router__main";
import LoginForm from "./Forms__Login.vue";

const resultIsReady = ref(false);

const onLogin = async ({ formData: { username, password }, setErrors }) => {
  try {
    resultIsReady.value = false;
    const { login } = useAuthStore();
    const successfulLogin = await login(username, password);
    router.push({ name: successfulLogin ? "route-list" : "route-login" });
  } catch (error) {
    setErrors({ apiError: error });
  } finally {
    resultIsReady.value = true;
  }
};
</script>
