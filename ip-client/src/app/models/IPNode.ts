export interface IPNode {
    args: string[];
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
}