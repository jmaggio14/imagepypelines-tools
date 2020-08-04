import { NodeService } from 'rete-angular-render-plugin';
import { Injectable } from '@angular/core';
import { IPGraph } from '../models/IPGraph';
import { of, Observable } from 'rxjs';
import * as mockGraph from './mock/graph.json';

@Injectable({providedIn: 'root'})
export class DashboardService {
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