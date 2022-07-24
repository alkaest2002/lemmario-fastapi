<template>
  <Form
    v-slot="{ errors, isSubmitting, values: { lemma, definition }, setErrors }"
    :validation-schema="validationSchema"
    :initial-values="initialValues"
    @submit="onSubmitForm"
    @invalid-submit="onInvalidSubmitForm"
  >
    <div class="field">
      <label class="label">Lemma</label>
      <div class="control">
        <Field
          name="lemma"
          type="text"
          class="input is-medium"
          placeholder="lemma"
          :class="{ 'is-danger': errors.lemma }"
        />
        <div class="has-text-danger">
          {{ errors.lemma }}
        </div>
      </div>
    </div>
    <div class="field">
      <label class="label">Definizione lemma</label>
      <div class="control">
        <Field
          as="textarea"
          name="definition"
          class="input is-medium"
          placeholder="Definizione lemma"
          :class="{ 'is-danger': errors.definition }"
        />
        <div class="has-text-danger">
          {{ errors.definition }}
        </div>
      </div>
    </div>
    <div class="control mt-5">
      <div class="buttons are-medium">
        <button class="button is-primary" @click="$router.go(-1)">
          &larr;
        </button>
        <base-loading-button
          v-model="isLoading"
          :type="'submit'"
          :button-css="'is-info'"
          :disabled="isSubmitting || !(lemma && definition)"
        >
          <slot name="upsertButtonLabel" />
        </base-loading-button>
        <base-loading-button
          v-model="isLoading"
          :button-css="'is-danger'"
          :disabled="isSubmitting || !(lemma && definition)"
          @click="onDeleteLemma(setErrors)"
        >
          Elimina
        </base-loading-button>
      </div>
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
    required: true,
  },
});

const emit = defineEmits({
  "on-upsert-lemma": null,
  "on-delete-lemma": null,
});

configure({
  validateOnBlur: false,
  validateOnChange: true,
  validateOnInput: false,
  validateOnModelUpdate: true,
});

const validationSchema = object().shape({
  lemma: string().required("lemma richiesto"),
  definition: string().required("definizione richiesta"),
});

const isLoading = ref(false);

watch(
  () => props.resultIsReady,
  (value) => {
    if (value) isLoading.value = false;
  }
);

const onSubmitForm = async (formData, { setErrors }) => {
  emit("on-upsert-lemma", { formData, setErrors });
};

const onDeleteLemma = async (setErrors) => {
  emit("on-delete-lemma", { setErrors });
};

const onInvalidSubmitForm = () => {
  isLoading.value = false;
};

onMounted(() => {
  const el = document.getElementsByTagName("textarea")[0];
  el.style.height = `${el.scrollHeight + 20}px`;
});
</script>
