import { Component, Input, AfterViewInit, ViewChild, ElementRef } from "@angular/core";
import { DashboardService } from "./dashboard-service";
import { Network } from "vis-network/peer/esm/vis-network";
import { DataSet } from "vis-data/peer/esm/vis-data"
import { IPGraph } from '../models/IPGraph';
import { IPWrapper} from '../models/IPWrapper';
import { IPStatus } from '../models/IPStatus';

@Component({
    selector: 'app-dashboard',
    templateUrl: './dashboard.component.html',
    styleUrls: ['./dashboard.component.css'],
    providers: [DashboardService]
  })
export class DashboardComponent {

  /**
   * UUID of this rete dashboard's session
   */
  @Input()
  public session: string;

  /**
   * The Vis Network
   */
  public network;

  @ViewChild('network')
  private networkNode: ElementRef;

  /**
   * IP Graph storage for this session
   */
  private graph: IPGraph;

  private insertedStatusUUIDs: string[] = [];

  /**
   * Constructor
   * @param dashboardService dashbaord service
   */
  public constructor(private dashboardService: DashboardService) {
    // subscribes to events emitted from the socket under 'status' type.
    // When a status message is received, we must wait to see if we have a graph rendered, then
    // we append it to the graph and rerender.
    dashboardService.subscribeToWebsocket('status', (statusWrapper: IPWrapper) => {
      const waitForGraph = setInterval(() => {
        if (this.networkNode && this.graph) {
          clearInterval(waitForGraph);
          if (this.appendStatusToGraph(statusWrapper)) {
            this.render(this.graph);
          }
        }
      }, 100);
    });
  }
  
  public ngAfterViewInit(): void {
    // grab the graph, grab any status that has been rendered
    // todo: this can be optimized so calls happen at the same time
    this.dashboardService.getPipelineData(this.session, 'graph').toPromise()
      .then((graph: IPWrapper) => {
        this.graph = graph.payload as IPGraph;
        return this.dashboardService.getPipelineData(this.session, 'status').toPromise();
      }).then((statuses: IPWrapper[]) => {
        statuses.forEach((status: IPWrapper) => this.appendStatusToGraph(status));
        this.render(this.graph);
      });
  }

  /**
   * Takes the status and inserts them into the graph
   * @param wrapper the status message
   * @returns true if they were inserted, false if they exist already.
   */
  public appendStatusToGraph(wrapper: IPWrapper): boolean {
    if (this.insertedStatusUUIDs.includes(wrapper.uuid)) {
      return false;
    }
    const status = wrapper.payload as IPStatus;
    // splice nodes and edges of status into graph
    Object.keys(status.nodes).forEach((key: string): void => {
      this.graph.nodes[key] = status.nodes[key];
    });
    Object.keys(status.edges).forEach((key: string): void => {
      this.graph.edges[key] = status.edges[key];
    });
    this.insertedStatusUUIDs.push(wrapper.uuid);
    return true;
  }

  public render(graph: IPGraph): void {
    const nodes = this.dashboardService.getGraphNodes(graph);
    const edges = this.dashboardService.getGraphEdges(graph);
    const data = { nodes, edges };

    const options = {
      layout: {
        hierarchical: {
          enabled: true,
          direction: "LR",
          sortMethod: "directed",
          blockShifting: true,
          edgeMinimization: false,
          levelSeparation: 100,
          nodeSpacing: 300,
          shakeTowards: 'roots'
        },
      },
    };

    // initialize your network!
    this.network = new Network(this.networkNode.nativeElement, data, options);
    this.network.redraw();
  }
}