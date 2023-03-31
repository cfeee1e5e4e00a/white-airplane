import ky from 'ky';

export const rest = ky.create({
    prefixUrl: `http://${import.meta.env.VITE_APP_BASE}`,
});
