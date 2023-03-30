import { FC } from 'react';

type Props = {
    id: number;
};

export const Supply: FC<Props> = ({ id }) => {
    return (
        <div className="flex flex-col border-2 border-black p-1 w-fit h-min gap-1 items-center">
            <h2 className="text-xl font-semibold">БП{id}</h2>
            <div className="dropdown dropdown-hover w-full">
                <label
                    tabIndex={0}
                    className="font-medium text-lg cursor-pointer break-keep w-full"
                >
                    <span>
                        P<sub>in</sub> = 2 Вт/ч
                    </span>
                </label>
                <div
                    tabIndex={0}
                    className="dropdown-content card card-compact w-40 p-2 shadow bg-primary-content flex items-center justify-center"
                >
                    <span>график</span>
                </div>
            </div>
            <div className="dropdown dropdown-hover w-full">
                <label
                    tabIndex={0}
                    className="font-medium text-lg cursor-pointer break-keep w-full"
                >
                    <span>
                        P<sub>out</sub> = 2 Вт/ч
                    </span>
                </label>
                <div
                    tabIndex={0}
                    className="dropdown-content card card-compact w-40 p-2 shadow bg-primary-content flex items-center justify-center"
                >
                    <span>график</span>
                </div>
            </div>
            <label className="font-medium text-lg cursor-pointer break-keep w-full">
                <span>η = 2 %</span>
            </label>
        </div>
    );
};
