import { createRouter, createWebHistory } from "vue-router";

import { useAuthStore } from "./store__auth";
import HomeView from "./views/HomeView.vue"
import LoginView from "./views/LoginView.vue";

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  linkActiveClass: "active",
  routes: [
    { name: "route-home", path: "/", component: HomeView },
    { name: "route-login",path: "/login", component: LoginView }
  ]
});

router.beforeEach(async (to) => {
  const publicPages = ["/login"];
  const authRequired = !publicPages.includes(to.path);
  const auth = useAuthStore();
  if (!authRequired && auth.isLoggedIn)
    return { name: "route-home" };
  if (authRequired && !auth.isLoggedIn) {
    auth.returnUrl = to.fullPath;
    return { name: "route-login" };
  }
});