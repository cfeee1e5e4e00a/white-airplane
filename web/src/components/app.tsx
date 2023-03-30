import { FC } from 'react';
import { BrowserRouter } from 'react-router-dom';
import { Router } from '@/components/router';

import '@/index.css';

export const App: FC = () => {
    return (
        <BrowserRouter>
            <Router />
        </BrowserRouter>
    );
};
