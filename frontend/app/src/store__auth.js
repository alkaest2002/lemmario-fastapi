import { defineStore } from "pinia";

import { fetchWrapper } from "./utils__fetch";
import { router } from "./router__main";

const baseUrl = import.meta.env.VITE_API_URL;
const authUrl = `${baseUrl}/utenti/login`;
const accessToken = localStorage.getItem("accessToken");

export const useAuthStore = defineStore({
  id: "auth",
  
  state: () => ({
    accessToken: accessToken ? JSON.parse(accessToken) : null,
    returnUrl: null
  }),

  getters: {
    isLoggedIn: (state) => state.accessToken != null
  },
  
  actions: {
    async login(username, password) {
      const { access_token: accessToken } = await fetchWrapper.post(authUrl, { username, password });
      this.accessToken = accessToken;
      localStorage.setItem("accessToken", JSON.stringify(accessToken));
      router.push(this.returnUrl || "/");
    },
    
    logout() {
      this.accessToken = null;
      localStorage.removeItem("accessToken");
      router.push({ name: "login" });
    }
  }
});