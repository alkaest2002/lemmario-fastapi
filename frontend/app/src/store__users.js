import { defineStore } from "pinia";

const state = () => ({
  isLogged: false,
  token: null,
});

export const useUserStore = defineStore("userStore", {
  state,

  persist: {
    storage: window.localStorage,
  },

  actions: {
    setIsLogged(isOnline) {
      this.isOnline = isOnline;
    },
  },
});
