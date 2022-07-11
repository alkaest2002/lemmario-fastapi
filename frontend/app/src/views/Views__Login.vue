<template>
  <div>
    <h2 class="is-size-2 has-text-weight-bold mb-4">Login</h2>
    <Form
      v-slot="{ errors, isSubmitting, setErrors }"
      :validation-schema="schema"
      @submit.prevent=""
    >
      <div class="field">
        <label class="label">Email</label>
        <div class="control">
          <Field
            v-model="username"
            name="username"
            type="text"
            class="input"
            placeholder="mario.rossi@mail.com"
            :class="{ 'is-danger': errors.username }"
          />
          <div class="has-text-danger">
            {{ errors.username }}
          </div>
        </div>
      </div>
      <div class="field">
        <label class="label">Password</label>
        <div class="control">
          <Field
            v-model="password"
            name="password"
            type="password"
            class="input"
            placeholder="password di mario rossi"
            :class="{ 'is-danger': errors.password }"
          />
          <div class="has-text-danger">
            {{ errors.password }}
          </div>
        </div>
      </div>
      <div class="field">
        <div class="control">
          <base-loading-button
            v-model="isLoading"
            :button-css="'is-info'"
            :disabled="isSubmitting || !(username && password)"
            @click="onSubmit(setErrors)"
          >
            Effettua login
          </base-loading-button>
        </div>
      </div>
      <div v-if="errors.apiError" class="has-text-danger mt-3 mb-0">
        {{ errors.apiError }}
      </div>
    </Form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { configure, Form, Field } from "vee-validate";
import { object, string } from 'yup';

import { useAuthStore } from "../store__auth";
import { router } from "../router__main";

const schema = object().shape({
  username: string().email("email non valida").required("email richiesta"),
  password: string().required("password richiesta"),
});

configure({
  validateOnBlur: false,
  validateOnChange: true,
  validateOnInput: false,
  validateOnModelUpdate: true,
});

const isLoading = ref(false);
const username = ref("");
const password = ref("");

const onSubmit = async (setErrors) => {
  if (!(username.value && password.value)) {
    isLoading.value = false;
    return;
  }
  try {
    const authStore = useAuthStore();
    const successfulLogin = await authStore.login(
      username.value,
      password.value
    );
    router.push({ name: successfulLogin ? "route-home" : "route-login" });
  } catch (error) {
    setErrors({ apiError: error });
  } finally {
    isLoading.value = false;
  }
};
</script>
