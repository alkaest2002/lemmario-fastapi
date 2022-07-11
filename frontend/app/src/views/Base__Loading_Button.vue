<template>
  <button
    class="button"
    :class="buttonCSSClass"
    :disabled="disabled"
    :type="buttonType"
    @click="$emit('update:modelValue', true)"
  >
    <slot />
  </button>
</template>

<script>
export default {
  name: "LoadingButton",
};
</script>

<script setup>
/* eslint-disable no-unused-vars, no-undef */
import { computed } from "vue";

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },

  buttonCss: {
    type: String,
    default: "",
  },

  buttonType: {
    type: String,
    default: "button",
  },

  disabled: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits({
  "update:modelValue": (value) => typeof value == "boolean",
});

const buttonCSSClass = computed(
  () => `${props.buttonCss} ${props.modelValue ? "is-loading" : null}`
);
</script>
