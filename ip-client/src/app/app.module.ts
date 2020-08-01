import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ReteComponent } from './rete/rete.component';
import { ReteModule } from 'rete-angular-render-plugin';
import { NumberComponent } from './rete/controls/number-control';
import { MyNodeComponent } from './rete/components/node/node.component';

@NgModule({
  declarations: [
    AppComponent,
    ReteComponent,
    NumberComponent,
    MyNodeComponent
  ],
  imports: [
    AppRoutingModule,
    BrowserModule,
    ReteModule
  ],
  providers: [],
  bootstrap: [AppComponent],
  entryComponents: [NumberComponent, MyNodeComponent]
})
export class AppModule {}