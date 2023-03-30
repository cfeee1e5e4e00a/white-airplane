import { StrictMode } from 'react';
import ReactDOM from 'react-dom/client';

import { App } from '@/components/app';

const root = document.querySelector<HTMLElement>('#root')!;

ReactDOM.createRoot(root).render(
    <StrictMode>
        <App />
    </StrictMode>
);
