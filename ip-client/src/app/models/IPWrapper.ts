import { IPGraph } from "./IPGraph";
import { IPError } from "./IPErrors";

export class IPWrapper {
    type: 'graph' | 'error' | 'reset' | 'status';
    name: string;
    id: string;
    uuid: string;
    source_type: string;
    payload: IPStatus | IPGraph | IPError;

    public constructor(data: any) {
        Object.assign(this, data);
    }
}