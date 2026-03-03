import { createRouter, createWebHistory } from 'vue-router'
import CreateView from '../views/CreateView.vue'
import PasteView from '../views/PasteView.vue'

const routes = [
  { path: '/', component: CreateView },
  { path: '/p/:id', component: PasteView },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
