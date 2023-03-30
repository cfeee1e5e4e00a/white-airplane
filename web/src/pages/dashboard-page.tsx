import { FC } from 'react';
import { ChevronDownIcon } from '@heroicons/react/20/solid';
import { Flat } from '@/components/flat';
import { Supply } from '@/components/supply';

export const DashboardPage: FC = () => {
    return (
        <div className="flex flex-col h-full w-full">
            <header className="navbar border-b border-gray-200">
                <h1 className="navbar-start text-2xl font-medium">Панель управления</h1>
                <div className="navbar-end">
                    <div className="dropdown dropdown-end">
                        <label
                            className="cursor-pointer text-xl flex flex-row items-center gap-1"
                            tabIndex={0}
                        >
                            <span>Максим</span>
                            <ChevronDownIcon className="h-5 w-5" />
                        </label>
                        <ul
                            className="dropdown-content menu menu-compact p-2 shadow bg-base-100 rounded-lg w-52"
                            tabIndex={0}
                        >
                            <li>
                                <a>Настройки</a>
                            </li>
                            <li>
                                <a>Выйти</a>
                            </li>
                        </ul>
                    </div>
                </div>
            </header>
            <main className="w-full flex-grow p-4 flex flex-col justify-between gap-12 py-12">
                <section className="flex flex-row justify-center w-full gap-24 px-24 text-3xl font-medium">
                    <span className="border-2 border-black p-1">P = 52 Вт/ч</span>
                    <span className="border-2 border-black p-1">$ = 15000 руб</span>
                </section>
                <section className="flex flex-row justify-between w-full px-24">
                    {Array.from({ length: 3 }).map((_, idx) => (
                        <Supply id={idx} key={idx} />
                    ))}
                </section>
                <section className="grid grid-cols-7 grid-rows-2 gap-y-8 place-items-center">
                    {Array.from({ length: 14 }).map((_, idx) => (
                        <Flat id={idx} key={idx} />
                    ))}
                </section>
            </main>
        </div>
    );
};
