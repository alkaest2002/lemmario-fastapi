<template>
  <div>
    <base-title :title="'Login'" />
    <Form
      v-slot="{ errors, isSubmitting, values: { username, password } }"
      :validation-schema="validationSchema"
      :initial-values="{
        username: 'p.calanna@gmail.com',
        password: '',
      }"
      @submit="onSubmitForm"
    >
      <div class="field">
        <label class="label">Email</label>
        <div class="control">
          <Field
            name="username"
            type="text"
            class="input is-medium"
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
            name="password"
            type="password"
            class="input is-medium"
            placeholder="password di mario rossi"
            :class="{ 'is-danger': errors.password }"
          />
          <div class="has-text-danger">
            {{ errors.password }}
          </div>
        </div>
      </div>
      <div class="control mt-5">
        <base-loading-button
          v-model="isLoading"
          :type="'submit'"
          :button-css="'is-medium is-info'"
          :disabled="isSubmitting || !(username && password)"
        >
          Effettua login
        </base-loading-button>
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
import { object, string } from "yup";

import { useAuthStore } from "../store__auth";
import { router } from "../router__main";

configure({
  validateOnBlur: false,
  validateOnChange: true,
  validateOnInput: false,
  validateOnModelUpdate: true,
});

const validationSchema = object().shape({
  username: string().email("email non valida").required("email richiesta"),
  password: string().required("password richiesta"),
});

const isLoading = ref(false);

const onSubmitForm = async ({ username, password }, { setErrors }) => {
  try {
    const { login } = useAuthStore();
    const successfulLogin = await login(username, password);
    router.push({ name: successfulLogin ? "route-list-lemmi" : "route-login" });
  } catch (error) {
    setErrors({ apiError: error });
  } finally {
    isLoading.value = false;
  }
};
</script>
