export class IPNode {
    args: string[];
    uuid: string;
    outputs: string[];
    validation_time: string;
    processing_time: string;
    num_in: number;
    n_batches: number;
    pid: number;
    status: string;
    name: string;
    shape: string;
    class_name: string;
    batch_type: string;


    public static fromJS(data: { [id: string]: any}): { [id: string]: IPNode} {
        const transformedEdges = JSON.parse(JSON.stringify(data));
        Object.keys(data).forEach((key: string): IPNode => {
            transformedEdges[key].uuid = key
            return;
        });
        return transformedEdges;
    }
}