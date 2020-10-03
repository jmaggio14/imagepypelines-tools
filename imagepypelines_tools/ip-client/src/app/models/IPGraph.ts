import { IPBlockDoc } from "./IPBlockDoc";
import { IPNode } from "./IPNode";
import { IPEdge } from "./IPEdge";

export interface IPGraph {
    args: string[];
    block_docs:  { [id: string]: IPBlockDoc}
    nodes:  { [id: string]: IPNode}
    edges:  { [id: string]: IPEdge};
    'node-link': any;
}