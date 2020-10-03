import { IPNode } from "./IPNode";
import { IPEdge } from "./IPEdge";

export interface IPStatus {
    nodes:  { [id: string]: IPNode}
    edges:  { [id: string]: IPEdge}
}