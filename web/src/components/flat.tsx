import { FC } from 'react';

type Props = {
    id: number;
    poweredBy: number;
    consumption: number;
    temperature: number;
    humidity: number;
    supplies: number[];
};

export const Flat: FC<Props> = ({
    id,
    consumption,
    temperature,
    humidity,
    poweredBy,
    supplies,
}) => {
    return (
        <div className="flex flex-col border-2 border-black p-1 w-fit h-min gap-1 items-center">
            <h2 className="text-xl font-semibold">К{id}</h2>
            <div className="flex flex-row items-center justify-between w-full">
                <div className="dropdown dropdown-hover">
                    <label tabIndex={0} className="font-medium text-lg cursor-pointer">
                        <span>P = {consumption.toFixed(0)} Вт/ч</span>
                    </label>
                    <div
                        tabIndex={0}
                        className="dropdown-content card card-compact w-40 p-2 shadow bg-primary-content flex items-center justify-center"
                    >
                        <span>график</span>
                    </div>
                </div>
                <input type="checkbox" className="toggle toggle-success" />
            </div>
            <label tabIndex={0} className="font-medium text-lg cursor-pointer w-full">
                <span>t = {temperature.toFixed(0)} °C</span>
            </label>
            <label tabIndex={0} className="font-medium text-lg cursor-pointer w-full">
                <span>φ = {humidity.toFixed(0)} %</span>
            </label>
            <div className="btn-group">
                {supplies.map((supply) => (
                    <input
                        type="radio"
                        name={`flat-${id}-poweredBy`}
                        data-title={`БП${supply}`}
                        checked={supply == poweredBy}
                        onChange={() => {}}
                        className="btn btn-sm btn-outline"
                        key={supply}
                    />
                ))}
            </div>
        </div>
    );
};
