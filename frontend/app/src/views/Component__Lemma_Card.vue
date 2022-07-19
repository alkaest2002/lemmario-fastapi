<template>
  <div
    class="card my-2 is-clickable"
    @click="
      emit('on-select-lemma', {
        lemma,
        isExpanded: isSelected && isOverFlown,
        isOverFlown,
      })
    "
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
        :class="{ 'is-expanded': isSelected && isOverFlown }"
        v-html="lemma.definition"
      />
    </div>
  </div>
</template>

<script setup>
/* eslint-disable no-unused-vars */
import { ref, computed, onMounted, onUnmounted } from "vue";

const emit = defineEmits({
  "on-select-lemma": (value) => typeof value == "object",
});

const props = defineProps({
  lemma: {
    type: Object,
    required: true,
  },

  selectedLemmaId: {
    type: [Number, null],
    default: null,
  },
});

const defintionParagraph = ref(null);

const isOverFlown = ref(false);

const markAsOverflownIfNecessary = () => {
  const { clientHeight, scrollHeight } = defintionParagraph.value;
  isOverFlown.value = scrollHeight > clientHeight;
};

const isSelected = computed(() => props.selectedLemmaId == props.lemma.rowid);

onMounted(() => {
  markAsOverflownIfNecessary(defintionParagraph.value);
  window.addEventListener("resize", markAsOverflownIfNecessary);
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
