import { FC } from 'react';
import { BrowserRouter } from 'react-router-dom';
import { ApolloProvider } from '@apollo/client';
import { Router } from '@/components/router';
import { graphqlClient } from '@/api/graphql';

import '@/index.css';

export const App: FC = () => {
    return (
        <ApolloProvider client={graphqlClient}>
            <BrowserRouter>
                <Router />
            </BrowserRouter>
        </ApolloProvider>
    );
};
