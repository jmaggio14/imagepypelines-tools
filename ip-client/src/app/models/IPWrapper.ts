import { IPGraph } from "./IPGraph";
import { IPError } from "./IPErrors";

export interface IPWrapper {
    type: 'graph' | 'error' | 'reset' | 'status';
    name: string;
    id: string;
    uuid: string;
    source_type: string;
    payload: {} | IPGraph | IPError;
}