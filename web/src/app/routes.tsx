import { RouteObject } from 'react-router-dom';

import { LoginPage } from '@/pages/login-page';
import { DashboardPage } from '@/pages/dashboard-page';

export const routes: RouteObject[] = [
    { index: true, element: <DashboardPage /> },
    { path: '/login', element: <LoginPage /> },
];
