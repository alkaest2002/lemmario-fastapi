<template>
  <Form
    v-slot="{ errors, isSubmitting, values: { username, password } }"
    :validation-schema="validationSchema"
    :initial-values="initialValues"
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
</template>

<script setup>
/* eslint-disable no-unused-vars */
import { ref, watch, onMounted } from "vue";
import { configure, Form, Field } from "vee-validate";
import { object, string } from "yup";

const props = defineProps({
  resultIsReady: {
    type: Boolean,
    default: false,
  },

  initialValues: {
    type: Object,
    required: true
  },
});

const emit = defineEmits({
  "on-login": (value) => {
    const c1 = Object.keys(value).every((key) => ["formData", "setErrors"].includes(key));
    const c2 = Object.keys(value.formData).every((key) => ["username", "password"].includes(key));
    return c1 && c2;
  },
});

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

watch(
  () => props.resultIsReady,
  (value) => {
    if (value) isLoading.value = false;
  }
);

const onSubmitForm = async ({ username, password }, { setErrors }) => {
  emit("on-login", { formData: { username, password }, setErrors });
};

onMounted(() => {
  const lemmaInput = document.getElementsByTagName("button")[0];
  lemmaInput.focus();
});
</script>
