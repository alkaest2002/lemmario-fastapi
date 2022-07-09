import { createApp } from "vue";
import { createPinia } from "pinia";
import { router } from "./router__main";

import App from "./App.vue";

const app = createApp(App);

app.use(createPinia()).use(router);

app.mount("#app");
