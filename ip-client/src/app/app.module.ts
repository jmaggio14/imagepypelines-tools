import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MaterialModule } from './material.module';
import { DocumentationComponent } from './documentation/documentation.component'
import {MatNativeDateModule} from '@angular/material/core';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { DashboardComponent } from './dashboard/dashboard.component';
import { SocketIoModule } from 'ngx-socket-io';
import { NgTerminalModule } from 'ng-terminal';
const thisUrl = window.location.href.split('/');

@NgModule({
  declarations: [
    AppComponent,
    DocumentationComponent,
    DashboardComponent
  ],
  imports: [
    AppRoutingModule,
    BrowserModule,
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    HttpClientModule,
    MatNativeDateModule,
    ReactiveFormsModule,
    MaterialModule,
    NgTerminalModule,
    // SocketIoModule.forRoot({
    //   url: thisUrl[0] + '//' + thisUrl[2] + ':' + 5000
    // })
  ],
  providers: [],
  bootstrap: [AppComponent],
  entryComponents: [DocumentationComponent]
})
export class AppModule {}