import { NodeService } from 'rete-angular-render-plugin';
import { Injectable, EventEmitter } from '@angular/core';
import { IPGraph } from '../models/IPGraph';
import { of, Observable } from 'rxjs';
import * as mockGraph from './mock/graph.json';
import { IPWrapper } from '../models/IPWrapper';

/**
 * The Imagepypeline service establishes a websocket with
 * this UI. The data is constantly emitted as it comes through
 * the pypelines module. 
 */
@Injectable({providedIn: 'root'})
export class DashboardService {

    private ipEventEmitter = new EventEmitter<IPWrapper>();
    

    /**
     * Establishes websocket connection
     */
    public constructor() {

    }

    /**
     * Subscribes to a websocket supplied by the commandline
     * @todo add express service and retrieve commandline argument for location
     */
    public subscribeToWebsocket() {
        const socket = new WebSocket();
        socket.
    }

    /**
     * Retrieves a graph by it's UUID from the pypeline service
     * @param uuid the uuid of the graph to retrieve
     */
    public getIPGraph(uuid: string): Observable<IPGraph> {
        //TODO
        return of(mockGraph);
    }

    /**
     * Take's an IP Graph and converts it to a rete.js graph
     * @param ipGraph an image pypeline's graph
     */
    public convertToReteNodeGraph(ipGraph: IPGraph) {
        // TODO
    }
}