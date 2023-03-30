import { signal } from '@preact/signals-react';

type Role = 'admin' | 'moderator' | 'user';

type User = {
    username: string;
    role: Role;
};

type Login = Logon | LoggedOut;
type Logon = { status: 'logon'; user: User };
type LoggedOut = { status: 'logged-out' };

export const login = signal<Login>({ status: 'logged-out' });
