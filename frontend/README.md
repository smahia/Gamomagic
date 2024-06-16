# How to

## Backend connection

You can customize it in the `.env` file. **Only requiered for local development**. The `BACKEND_HOST` and `BACKEND_PORT` affects to the `src/environments/environment.ts` which affects to `src/app/search/search.service.ts` file.

If you need to add more variables, be aware of they need to be declared first in the `env.d.ts` file.

Also, take care of this part of the `angular.json` file:

```json
"ngxEnv": {
  "prefix": "^BACKEND_"
},
```

Which says: "all environment variables must be prefixed with BACKEND_" in case you need to change it.

## Install Angular

Run `npm install -g @angular/cli` only the very first time.

## Install dependencies

Run `npm install` only the very first time.

## Development server

Run `npm start` or `ng serve --open` for a dev server. Navigate to `http://localhost:4200/`. The application will automatically reload if you change any of the source files.

## Development server with fake service

Run `npm install -g json-server` only the very first time.
Run `json-server --watch db.json` when you want to fake the service. It looks for a `db.json` file in the root of your project.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via a platform of your choice. To use this command, you need to first add a package that implements end-to-end testing capabilities.
