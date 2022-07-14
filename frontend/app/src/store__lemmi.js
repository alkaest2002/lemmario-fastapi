import { defineStore } from "pinia";
import { fetchWrapper } from "./utils__fetch";
import { lemmiUrl } from "./utils__urls";

const { get } = fetchWrapper;

export const useLemmiStore = defineStore({
  id: "lemmi",

  state: () => ({
    currentPageNumber: 1,
    currentSelectedLemmaId: null,
    currentPage: {
      data: [],
      metadata: {
        filter_by: null,
        filter_value: null,
        order_by: "lemma",
        order_value: "ASC",
        page_dir: "NEXT",
        page_size: 10,
        offset: null,
      },
    },
  }),

  getters: {
    currentSelectedLemma: (state) => {
      if (!state.currentSelectedLemmaId) return null;
      return state.currentPage.data.find(
        (elm) => elm.rowid == state.currentSelectedLemmaId
      );
    },
  },

  actions: {
    async fetchLemmi() {
      const payload = Object.keys(this.currentPage.metadata).reduce(
        (acc, itr) => {
          if (this.currentPage.metadata[itr])
            acc[itr] = this.currentPage.metadata[itr];
          return acc;
        },
        {}
      );
      try {
        const page = await get(`${lemmiUrl}/list`, { payload });
        this.currentPage = page;
        return Promise.resolve(true);
      } catch (error) {
        return Promise.reject(error);
      }
    },

    currentExpandendItem(itemId) {
      this.currentSelectedLemmaId = itemId;
    },

    updateCurrentPageNumber(pageDirection) {
      this.currentPageNumber += pageDirection === "NEXT" ? +1 : -1;
    },
  },
});
