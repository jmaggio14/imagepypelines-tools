import { Injectable, EventEmitter } from '@angular/core';
import { IPGraph } from '../models/IPGraph';
import { of, Observable } from 'rxjs';
import { IPWrapper } from '../models/IPWrapper';
import { Socket } from 'ngx-socket-io';
import { HttpClient } from '@angular/common/http';
import { DataSet } from "vis-data/peer/esm/vis-data"

/**
 * The Imagepypeline service establishes a websocket with
 * this UI. The data is constantly emitted as it comes through
 * the pypelines module. 
 */
@Injectable({providedIn: 'root'})
export class DashboardService {
    
    private ipEventEmitter = new EventEmitter<IPWrapper>();
    private ipWrapper: Observable<IPWrapper[]> = this.socket.fromEvent<IPWrapper[]>('pipeline-update');

    /**
     * Establishes websocket connection
     * @param socket from dependency injection
     */
    public constructor(private socket: Socket, private http: HttpClient) {
        console.log('test');
        this.socket.on('pipeline-update', (ipMessage: any) => {
            console.log(ipMessage);
            this.ipEventEmitter.emit(ipMessage);
        });
    }

    /**
     * Subscribes to a websocket supplied by the commandline
     */
    public subscribeToWebsocket(
        type: 'all' | 'error' | 'pipeline' | 'status' | 'reset', 
        callback: (wrapper: IPWrapper) => void) {
            this.ipEventEmitter.subscribe((ipMessage: IPWrapper) => {
                if (ipMessage.type === type || type === 'all') {
                    callback(ipMessage);
                }
            });
        }

    /**
     * @todo Change host and port
     */
    public getAllSessions(): Observable<string[]> {
        return this.http.get<string[]>('http://localhost:5000/api/sessions');
    }

    public runPypeline(id: string): void {
        //TBD
    }
    
    /**
     * Take's an IP Graph and converts it to a vis.js graph
     * @param ipGraph an image pypeline's graph nodes
     */
    public getGraphNodes(ipGraph: IPGraph): DataSet<any> {
        return <any> Object.keys(ipGraph.nodes).map((nodeId: string) => {
            let node = ipGraph.nodes[nodeId] as any;
            node.id = nodeId;
            node.label = node.name;
            return node;
        });
    }

    /**
     * Takes an IP Graph and formats the edges to a vis.js edge set
     * @param ipGraph an image pypeline's graph nodes
     */
    public getGraphEdges(ipGraph: IPGraph): DataSet<any> {
        return <any> Object.keys(ipGraph.edges).map((id) => {
            let edge = ipGraph.edges[id] as any;
            edge.from = edge.in_index;
            edge.to = edge.out_index;
            return edge;
        });
    }
}