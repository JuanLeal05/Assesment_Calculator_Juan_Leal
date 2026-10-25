interface ImportMetaEnv {
  /** Base URL of the calculator API. Defaults to http://localhost:8000. */
  readonly VITE_API_URL?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
