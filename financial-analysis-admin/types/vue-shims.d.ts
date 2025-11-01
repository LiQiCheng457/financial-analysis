// Type declarations for .vue files and some third-party libs used in the project
declare module '*.vue' {
  import { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

// If the project uses the `vite-plugin-svg-icons` client helper
declare module 'vite-plugin-svg-icons/client' {
  export function loadSvgComponent(id: string): any
  const _default: any
  export default _default
}

// Simple fallback typing for qrcode library when @types/qrcode is not installed
declare module 'qrcode' {
  export function toDataURL(text: string, options?: any): Promise<string>
  export function toCanvas(canvas: HTMLCanvasElement, text: string, options?: any): Promise<void>
  export function toString(text: string, options?: any): Promise<string>
}

// 为 element-plus/global 和 vite/client 提供声明以消除编辑器找不到类型定义文件的警告
declare module 'element-plus/global' {
  const _default: any
  export default _default
}

declare module 'vite/client' {
  interface ImportMetaEnv {
    readonly VITE_APP_TITLE: string
    // 可根据实际项目添加更多环境变量类型
  }

  interface ImportMeta {
    readonly env: ImportMetaEnv
  }
}
