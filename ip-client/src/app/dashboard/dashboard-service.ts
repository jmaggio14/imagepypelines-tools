import { Injectable, EventEmitter } from '@angular/core';
import { IPGraph } from '../models/IPGraph';
import { of, Observable } from 'rxjs';
import { IPWrapper } from '../models/IPWrapper';
import { Socket } from 'ngx-socket-io';
import { HttpClient } from '@angular/common/http';

/**
 * The Imagepypeline service establishes a websocket with
 * this UI. The data is constantly emitted as it comes through
 * the pypelines module. 
 */
@Injectable({providedIn: 'root'})
export class DashboardService {
    
    private ipEventEmitter = new EventEmitter<IPWrapper>();
    // private ipWrapper: Observable<IPWrapper[]> = this.socket.fromEvent<IPWrapper[]>('pipeline-update');

    /**
     * Establishes websocket connection
     * @param socket from dependency injection
     */
    public constructor(/*private socket: Socket,*/ private http: HttpClient) {
        // this.socket.on('pipeline-update', (ipMessage: IPWrapper) => {
        //     console.debug(ipMessage);
        //     this.ipEventEmitter.emit(ipMessage);
        // });
    }

    /**
     * Subscribes to a websocket supplied by the commandline
     */
    public subscribeToWebsocket(
        type: 'all' | 'error' | 'graph' | 'status' | 'reset', 
        callback: (wrapper: IPWrapper) => void) {
            this.ipEventEmitter.subscribe((ipMessage: IPWrapper) => {
                if (ipMessage.type === type || type === 'all') {
                    callback(ipMessage);
                }
            });
        }

    /**
     * @implNotes this will fail until we move the distribution to be inside the python app
     * @todo Change host and port
     */
    public getAllSessions(): Observable<string[]> {
        return this.http.get<string[]>('http://localhost:5000/api/sessions');
    }
    
    /**
     * Take's an IP Graph and converts it to a vis.js graph
     * @param ipGraph an image pypeline's graph
     */
    public convertToNodeGraph(ipGraph: IPGraph) {
        // TODO
    }
}