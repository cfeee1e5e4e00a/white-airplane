import { FC, useEffect } from 'react';
import { useNavigate, useRoutes } from 'react-router-dom';

import { routes } from '@/app/routes';
import { getAuthorizationToken } from '@/api/authorization-storage';

export const Router: FC = () => {
    const navigate = useNavigate();

    useEffect(() => {
        const token = getAuthorizationToken();

        if (!token) {
            navigate('/login');
        } else {
            navigate('/');
        }
    }, []);

    return useRoutes(routes);
};
