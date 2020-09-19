import { Component, Input, AfterViewInit, ViewChild, ElementRef } from "@angular/core";
import { DashboardService } from "./dashboard-service";
import { Network } from "vis-network/peer/esm/vis-network";
import { DataSet } from "vis-data/peer/esm/vis-data"
import { IPGraph } from '../models/IPGraph';
import { IPWrapper} from '../models/IPWrapper';

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
   * Constructor
   * @param dashboardService 
   */
  public constructor(private dashboardService: DashboardService) {
    dashboardService.subscribeToWebsocket('pipeline', (graph: IPWrapper) => {
      if (!this.networkNode) {
        return;
      }

      this.render(<IPGraph>(<unknown>graph));
    });
  }

  public render(graph: IPGraph): void {
    const nodes = this.dashboardService.getGraphNodes(graph);
    const edges = this.dashboardService.getGraphEdges(graph);
    const data = { nodes, edges };

    const options = {
      layout: {
        hierarchical: {
          sortMethod: 'directed'
        },
      },
    };

    // initialize your network!
    this.network = new Network(this.networkNode.nativeElement, data, options);
    this.network.redraw();
  }
}