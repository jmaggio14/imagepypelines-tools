import { IPDoc } from './IPDoc';
export class IPBlockDoc {
    name: string;
    id: string;
    uuid: string;
    args: string[];
    types:  { [name: string]: string}
    //?
    shapes: {}
    skip_enforcement: boolean;
    batch_type: string;
    class_name: string;
    tags: string[];
    DOCS: IPDoc;
}