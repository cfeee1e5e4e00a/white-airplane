import { getAuthorizationToken } from '@/api/authorization-storage';
import { ApolloClient, InMemoryCache } from '@apollo/client';
import { GraphQLWsLink } from '@apollo/client/link/subscriptions';
import { createClient } from 'graphql-ws';

const wsLink = new GraphQLWsLink(
    createClient({
        url: `ws://${import.meta.env.VITE_APP_BASE}/graphql`,
        connectionParams: {
            authToken: getAuthorizationToken(),
        },
    })
);

export const graphqlClient = new ApolloClient({
    link: wsLink,
    cache: new InMemoryCache(),
});
