import { Component, Input, AfterViewInit, ViewChild, ElementRef } from "@angular/core";
import { DashboardService } from "./dashboard-service";
import { Network } from "vis-network/peer/esm/vis-network";
import { DataSet } from "vis-data/peer/esm/vis-data"

@Component({
    selector: 'app-dashboard',
    templateUrl: './dashboard.component.html',
    styleUrls: ['./dashboard.component.css'],
    providers: [DashboardService]
  })
export class DashboardComponent implements AfterViewInit {

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

  }

  public render(): void {
    const nodes = new DataSet<any>([
        {id: 1, label: 'Node 1'},
        {id: 2, label: 'Node 2'},
        {id: 3, label: 'Node 3'},
        {id: 4, label: 'Node 4'},
        {id: 5, label: 'Node 5'}
    ]);

    const edges = new DataSet<any>([
        {from: 1, to: 3},
        {from: 1, to: 2},
        {from: 2, to: 4},
        {from: 2, to: 5}
    ]);
    const data = { nodes, edges };

    const options = {
      layout: {
        hierarchical: {
          sortMethod: 'layout-method-directed'
        },
      },
    };

    console.log(this.networkNode);
    // initialize your network!
    this.network = new Network(this.networkNode.nativeElement, data, options);
  }


  /**
   * Sets up graph
   */
  public ngAfterViewInit(): void {
    this.render();
  }
}