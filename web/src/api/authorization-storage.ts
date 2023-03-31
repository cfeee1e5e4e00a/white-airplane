export const getAuthorizationToken = (win = window): string | null => {
    return win.localStorage.getItem('Authorization');
};

export const setAuthorizationToken = (token: string, win = window): void => {
    win.localStorage.setItem('Authorization', token);
};
