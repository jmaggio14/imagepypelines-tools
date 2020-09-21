import { Component, ViewChild } from '@angular/core';
import { DashboardService } from './dashboard/dashboard-service';
import { NgTerminal, DisplayOption } from 'ng-terminal';
import { IPWrapper } from './models/IPWrapper';
import { IPError } from './models/IPErrors';
import { Socket } from 'ngx-socket-io';
import { MatDrawer } from '@angular/material/sidenav';
import { DashboardComponent } from './dashboard/dashboard.component';
import { IPStatus } from './models/IPStatus';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers: [DashboardService]
})
export class AppComponent {
  //private displayOptionsTerminal: DisplayOption = { activateDraggabcdleOnEdge: {}};

  @ViewChild('term', { static: true }) 
  private terminal: NgTerminal;

  @ViewChild('drawer', {static: false, read: MatDrawer})
  private drawer: MatDrawer;

  @ViewChild('dashboard', { static: false, read: DashboardComponent})
  private ipDashboard: DashboardComponent;

  // UUIDs of pypelines
  public sessions: string[] = [];

  mockDoc = {
      "name": "InputNone",
      "id": "InputNone#6fb745",
      "uuid": "75b1683e54924019b03d148e096fb745",
      "args": [],
      "types": {},
      "shapes": {},
      "skip_enforcement": false,
      "batch_type": "all",
      "tags": [],
      "class_name": "Input",
      "DOCS": {
          "class": "An object to inject data into the graph\n\nAttributes:\n    data(any type):\n    loaded(bool): where",
          "__init__": "instantiates the Input\n\nArgs:\n    index(int,None): index of the input into the Pipeline",
          "process": "returns the loaded data"
      }
  };

  public constructor(private dashboardService: DashboardService, private socket: Socket) {
    this.dashboardService.getAllSessions()
      .subscribe((sessions: string[]) => this. sessions = sessions);
  }

  public ngAfterViewInit(): void {
    //this.terminal.setStyle()
    this.terminal.write('Establishing connection to the pypeline service....');
    this.dashboardService.subscribeToWebsocket('error', (wrapper) => this.writeErrorMessageToTermianl(wrapper));
  }

  /**
   * Causes the documentation slider to open, and rerenders the graph
   */
  public documentationDrawerToggle(): void {
    this.drawer.toggle();
  }

  /**
   * Formats the error message and spits it out to the terminal
   * @param wrapper incoming IP Msg
   */
  private writeErrorMessageToTermianl(wrapper: IPWrapper): void {
    const error = wrapper.payload as IPError;
    const formattedMsg = `ERROR-${error.error_type}@${error.block_uuid}-${error.block_name}: ${error.error_msg}`;
    this.terminal.write(formattedMsg);
  }
}
