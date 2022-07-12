<template>
  <div class="card my-2 is-clickable" @click="emit('update:modelValue', lemma.rowid)">
    <div class="card-content">
      <p class="lemma is-size-5 has-text-weight-bold">
        {{ lemma.lemma }} {{ isOverFlown }}
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
 import { ref, computed, onMounted } from "vue";

const emit = defineEmits({
  "update:modelValue": value => typeof value == "number"
})

const props = defineProps({
  modelValue: {
    type: Number,
    default: null
  },

  lemma: {
    type: Object,
    required: true,
  }
});

const defintionParagraph = ref(null)

const isOverflown = (el) => {
  if (el) {
    const { clientHeight, scrollHeight } = el;
    return scrollHeight > clientHeight;
  }
  return false;
}

const isExpanded = computed(() => props.modelValue == props.lemma.rowid);

const isOverFlown = computed(() => isOverflown(defintionParagraph.value))

</script>

<style lang="scss" scoped>
  .card-content {

    .lemma {
      text-transform: uppercase;
    }
    
    > p:nth-child(2) {
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