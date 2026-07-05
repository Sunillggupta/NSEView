import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./pages/dashboard/dashboard.component').then((m) => m.DashboardComponent),
    title: 'NSE Indices Dashboard',
  },
  {
    path: 'index/:symbol',
    loadComponent: () =>
      import('./pages/index-detail/index-detail.component').then((m) => m.IndexDetailComponent),
    title: 'Index Details',
  },
  {
    path: 'about',
    loadComponent: () => import('./pages/about/about.component').then((m) => m.AboutComponent),
    title: 'About - NSE Data Dashboard',
  },
  {
    path: 'status',
    loadComponent: () => import('./pages/status/status.component').then((m) => m.StatusComponent),
    title: 'API Status',
  },
  { path: '**', redirectTo: '' },
];
