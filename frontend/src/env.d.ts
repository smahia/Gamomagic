interface ImportMeta {
  readonly env: ImportMetaEnv;
}
  
interface ImportMetaEnv {
  readonly BACKEND_SERVICE_HOST: string;
  readonly BACKEND_SERVICE_PORT: string;
}