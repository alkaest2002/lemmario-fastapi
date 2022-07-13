<template>
  <div
    class="card my-2 is-clickable"
    @click="emit('update:modelValue', lemma.rowid)"
  >
    <div class="card-content">
      <p class="lemma is-size-5 has-text-weight-bold">
        {{ lemma.lemma }}
      </p>
      <p v-if="isOverFlown" class="subtitle is-6 has-text-grey">
        clicca per espandere lemma
      </p>
      <p
        ref="defintionParagraph"
        class="definition"
        :class="{ 'is-expanded': isExpanded }"
      >
        {{ lemma.definition }}
      </p>
    </div>
  </div>
</template>

<script setup>
/* eslint-disable no-unused-vars */
import { ref, computed, onMounted, onUnmounted } from "vue";

const emit = defineEmits({
  "update:modelValue": (value) => typeof value == "number",
});

const props = defineProps({
  modelValue: {
    type: Number,
    default: null,
  },

  lemma: {
    type: Object,
    required: true,
  },
});

const defintionParagraph = ref(null);

const isOverFlown = ref(false);

const markAsOverflownIfNecessary = ({ clientHeight, scrollHeight }) => {
  isOverFlown.value = scrollHeight > clientHeight;
};

const isExpanded = computed(() => props.modelValue == props.lemma.rowid);

onMounted(() => {
  markAsOverflownIfNecessary(defintionParagraph.value);
  window.addEventListener("resize", () => {
    markAsOverflownIfNecessary(defintionParagraph.value);
  });
});

onUnmounted(() => {
  window.removeEventListener("resize", markAsOverflownIfNecessary);
});
</script>

<style lang="scss" scoped>
.card-content {
  .lemma {
    text-transform: uppercase;
  }

  > .definition {
    display: block;
    max-height: 145px;
    overflow: hidden;
    text-overflow: ellipsis;

    &.is-expanded {
      max-height: none;
      height: 100%;
    }
  }
}
</style>
