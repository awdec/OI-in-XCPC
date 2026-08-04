import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import { createRouter, createWebHashHistory } from 'vue-router'
import App from './App.vue'
import './assets/styles/main.css'

// 路由配置
const routes = [
  { path: '/', name: 'Home', component: () => import('./views/Home.vue') },
  { path: '/contest/:id', name: 'Contest', component: () => import('./views/Contest.vue'), props: true },
  { path: '/school/:name', name: 'School', component: () => import('./views/School.vue'), props: true },
  { path: '/player/:name', name: 'Player', component: () => import('./views/Player.vue'), props: true },
  { path: '/compare', name: 'Compare', component: () => import('./views/Compare.vue') },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

const app = createApp(App)
app.use(ElementPlus, { locale: zhCn })
app.use(router)
app.mount('#app')
