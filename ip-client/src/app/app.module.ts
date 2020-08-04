import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ReteComponent } from './rete/rete.component';
import { ReteModule } from 'rete-angular-render-plugin';
import { NumberComponent } from './rete/controls/number-control';
import { MyNodeComponent } from './rete/components/node/node.component';
import { MaterialModule } from './material.module';
import { DocumentationComponent } from './documentation/documentation.component'
import {MatNativeDateModule} from '@angular/material/core';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { DashboardComponent } from './dashboard/dashboard.component';
@NgModule({
  declarations: [
    AppComponent,
    ReteComponent,
    NumberComponent,
    MyNodeComponent,
    DocumentationComponent,
    DashboardComponent
  ],
  imports: [
    AppRoutingModule,
    BrowserModule,
    ReteModule,
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    HttpClientModule,
    MatNativeDateModule,
    ReactiveFormsModule,
    MaterialModule
  ],
  providers: [],
  bootstrap: [AppComponent],
  entryComponents: [NumberComponent, MyNodeComponent, DocumentationComponent]
})
export class AppModule {}