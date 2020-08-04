import { IPBlockDoc } from "./IPBlockDoc";

export interface IPGraph {
    block_docs: IPBlockDoc[];
    nodes: IPNode[];
    edges: IPEdge[];
}