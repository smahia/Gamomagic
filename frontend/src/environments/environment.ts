const host = import.meta.env.BACKEND_SERVICE_HOST;
const port = import.meta.env.BACKEND_SERVICE_PORT;

export const environment = {
  production: false,
  backendUrl: `${host}:` + `${port}`,
};