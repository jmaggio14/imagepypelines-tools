import { Component, Input } from '@angular/core';
import { IPBlockDoc } from '../models/IPBlockDoc';

@Component({
  selector: 'app-documentation',
  templateUrl: './documentation.component.html',
  styleUrls: ['./documentation.component.css']
})
export class DocumentationComponent {

  @Input()
  public documentation: IPBlockDoc;

  /**
   * Resets this class so there is no data to display
   */
  public reset(): void {
      this.documentation = undefined;
  }
}
