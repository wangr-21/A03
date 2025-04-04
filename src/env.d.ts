/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string;
  // 其他可能的环境变量
  [key: string]: unknown;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
