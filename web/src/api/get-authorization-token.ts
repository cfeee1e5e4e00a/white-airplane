export const getAuthorizationToken = (win = window) => {
    return win.localStorage.getItem('bearer');
};
