import { defineStore } from "pinia";
import { fetchWrapper } from "./utils__fetch";
import { lemmiUrl } from "./utils__urls";

const { get } = fetchWrapper;

export const useLemmiStore = defineStore({
  id: "lemmi",

  state: () => ({
    currentPageNumber: 1,
    currentSelectedLemma: null,
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

  actions: {
    async fetchLemmi(getCache = false) {
      const payload = Object.keys(this.currentPage.metadata).reduce(
        (acc, itr) => {
          if (this.currentPage.metadata[itr])
            acc[itr] = this.currentPage.metadata[itr];
          return acc;
        },
        {}
      );
      try {
        if (!getCache) {
          const page = await get(`${lemmiUrl}/list`, { payload });
          this.currentPage = page;
        }
        return Promise.resolve(true);
      } catch (error) {
        return Promise.reject(error);
      }
    },

    updateCurrentPageNumber(pageDirection) {
      this.currentPageNumber += pageDirection === "NEXT" ? +1 : -1;
    },

    updateLemma() {
      if (!this.currentSelectedLemma) return null;
      const lemmaIndex = this.currentPage.data.findIndex(
        (elm) => elm.rowid == this.currentSelectedLemma.rowid
      );
      if (lemmaIndex > -1)
       this.currentPage.data[lemmaIndex] = this.currentSelectedLemma;
    },
  },
});
