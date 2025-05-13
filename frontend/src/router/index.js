import { createRouter, createWebHistory } from "vue-router";
import ScheduleView from "../components/ScheduleView.vue";
import ScheduleEditor from "../components/ScheduleEditor.vue";

const routes = [
  { path: "/", name: "ScheduleView", component: ScheduleView },
  { path: "/editor", name: "ScheduleEditor", component: ScheduleEditor },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
