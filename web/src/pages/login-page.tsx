import { FC, FormEventHandler } from 'react';
import { Link } from 'react-router-dom';
import { useInput } from '@/hooks/useInput';
import { rest } from '@/api/rest';
import { setAuthorizationToken } from '@/api/authorization-storage';

export const LoginPage: FC = () => {
    const login = useInput();
    const password = useInput();

    const onSubmit: FormEventHandler = async (event) => {
        event.preventDefault();

        console.log(1);

        const token = await rest
            .post('login', {
                json: {
                    username: login.value,
                    password: password.value,
                },
            })
            .json<string>();

        setAuthorizationToken(token);

        window.location.reload();
    };

    return (
        <main className="w-full h-full flex items-center justify-center bg-base-100">
            <form
                className="w-80 flex flex-col items-center justify-start gap-2 border-2 border-zinc-200 rounded-2xl px-8 py-4 bg-primary-content"
                onSubmit={onSubmit}
            >
                <h1 className="text-3xl mb-4">Вход</h1>
                <div className="form-control w-full max-w-xs">
                    <label className="label">
                        <span className="label-text">Введите имя пользователя</span>
                    </label>
                    <input
                        className="input input-bordered w-full max-w-xs"
                        type="text"
                        placeholder="Логин"
                        {...login}
                    />
                </div>
                <div className="form-control w-full max-w-xs mb-4">
                    <label className="label">
                        <span className="label-text">Введите пароль</span>
                    </label>
                    <input
                        className="input input-bordered w-full max-w-xs"
                        type="password"
                        placeholder="Пароль"
                        {...password}
                    />
                </div>
                <Link className="link link-primary link-hover w-full mb-4" to="/register">
                    Зарегистрироваться
                </Link>
                <button className="btn btn-primary w-full">Войти</button>
            </form>
        </main>
    );
};
