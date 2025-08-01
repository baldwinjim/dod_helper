import { Routes } from '@angular/router';
import { Speakers } from './speakers/speakers';
import { Sponsors } from './sponsors/sponsors';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'speakers',
    pathMatch: 'full',
  },
  {
    path: 'speakers',
    component: Speakers,
  },
  {
    path: 'sponsors',
    component: Sponsors,
  },
];
