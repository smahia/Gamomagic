import { bootstrapApplication } from '@angular/platform-browser';
import { provideRouter } from '@angular/router';
import { provideAnimations } from '@angular/platform-browser/animations';
import { VERSION as CDK_VERSION } from '@angular/cdk';
import { VERSION as MAT_VERSION, MatNativeDateModule } from '@angular/material/core';
import { importProvidersFrom } from '@angular/core';

import { AppComponent } from './app/app.component';
import routeConfig from './app/routes';

/* eslint-disable no-console */
console.info('Angular CDK version', CDK_VERSION.full);
console.info('Angular Material version', MAT_VERSION.full);

bootstrapApplication(AppComponent,
  {
    providers: [
      provideAnimations(),
      provideRouter(routeConfig),
      importProvidersFrom(MatNativeDateModule)
    ]
  }
).catch(err => console.error(err));
