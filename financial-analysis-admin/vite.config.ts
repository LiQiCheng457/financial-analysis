import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import { fileURLToPath, URL } from 'node:url'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  // 加载环境变量
  const env = loadEnv(mode, process.cwd())
  
  return {
  plugins: [
    vue(),
    AutoImport({
      resolvers: [ElementPlusResolver()]
    }),
    Components({
      resolvers: [ElementPlusResolver()]
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: '0.0.0.0', // 允许外部访问
    port: 5173,
    strictPort: false, // 端口被占用时自动尝试下一个
    open: false, // 不自动打开浏览器
    cors: true, // 允许跨域
    hmr: {
      overlay: true // 错误覆盖层
    },
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        timeout: 30000 // 增加超时时间到30秒
      }
    }
  },
  // 预览服务器配置
  preview: {
    host: '0.0.0.0',
    port: 4173,
    strictPort: false,
    allowedHosts: [
      '.cpolar.top',  // 允许所有 cpolar 域名
      '.cpolar.cn',   // 允许所有 cpolar.cn 域名
      '.ngrok.io',    // 也支持 ngrok
      'localhost'
    ]
  },
  // 优化选项
  optimizeDeps: {
    include: ['vue', 'vue-router', 'pinia', 'element-plus', 'axios', 'echarts'] // 预构建依赖
  },
  build: {
    outDir: env.VITE_OUT_DIR || 'dist', // 从环境变量读取输出目录
    target: 'es2015', // 兼容性目标
    chunkSizeWarningLimit: 1500, // chunk 大小警告限制
    rollupOptions: {
      output: {
        manualChunks: {
          'element-plus': ['element-plus'],
          'echarts': ['echarts']
        }
      }
    }
  }
  }
})
