export class IPEdge {
    var_name: string;
    out_index: number;
    in_index: number;
    name: string;
    is_homogenus: boolean;
    n_items: number;
    in_uuid: string;
    out_uuid: string

    public static fromJS(data: { [id: string]: any}): { [id: string]: IPEdge} {
        const transformedEdges = JSON.parse(JSON.stringify(data));
        Object.keys(data).forEach((key: string): IPEdge => {
            if (data[key].in_uuid) {
                return;
            }
            const [in_uuid, out_uuid] = key.split('|');
            transformedEdges[key].in_uuid = in_uuid;
            transformedEdges[key].out_uuid = out_uuid;
            return;
        });
        return transformedEdges;
    }
}