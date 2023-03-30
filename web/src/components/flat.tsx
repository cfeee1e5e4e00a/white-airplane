import { FC } from 'react';

type Props = {
    id: number;
};

export const Flat: FC<Props> = ({ id }) => {
    return (
        <div className="flex flex-col border-2 border-black p-1 w-fit h-min gap-1 items-center">
            <h2 className="text-xl font-semibold">К{id}</h2>
            <div className="flex flex-row items-center justify-between w-full">
                <input type="checkbox" className="toggle toggle-success" />
                <div className="dropdown dropdown-hover">
                    <label tabIndex={0} className="font-medium text-lg cursor-pointer">
                        <span>2 Вт/ч</span>
                    </label>
                    <div
                        tabIndex={0}
                        className="dropdown-content card card-compact w-40 p-2 shadow bg-primary-content flex items-center justify-center"
                    >
                        <span>график</span>
                    </div>
                </div>
            </div>
            <div className="btn-group">
                <input
                    type="radio"
                    name="options"
                    data-title="БП1"
                    className="btn btn-sm btn-outline"
                />
                <input
                    type="radio"
                    name="options"
                    data-title="БП2"
                    className="btn btn-sm btn-outline"
                />
                <input
                    type="radio"
                    name="options"
                    data-title="БП3"
                    className="btn btn-sm btn-outline"
                />
            </div>
        </div>
    );
};
