import { createRouter, createWebHistory } from "vue-router";

import { useAuthStore } from "./store__auth";
import HomeView from "./views/Views__Home.vue";
import LoginView from "./views/Views__Login.vue";

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  linkActiveClass: "active",
  routes: [
    { name: "route-home", path: "/", component: HomeView },
    { name: "route-login", path: "/login", component: LoginView },
  ],
});

router.beforeEach(async (to) => {
  const auth = useAuthStore();
  const publicRoutes = ["route-login"];
  const authRequired = !publicRoutes.includes(to.name);
  if (!authRequired && auth.isLoggedIn) return { name: "route-home" };
  if (authRequired && !auth.isLoggedIn) {
    auth.returnUrl = to.fullPath;
    return { name: "route-login" };
  }
});
