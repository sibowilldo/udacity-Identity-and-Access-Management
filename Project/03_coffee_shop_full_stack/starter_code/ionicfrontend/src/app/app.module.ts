import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';
import {RouteReuseStrategy} from '@angular/router';

import {IonicModule, IonicRouteStrategy} from '@ionic/angular';
import {SplashScreen} from "@awesome-cordova-plugins/splash-screen/ngx";
import {StatusBar} from "@awesome-cordova-plugins/status-bar/ngx";

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';

import {DrinksService} from "@services/drinks.service";
import {AuthService} from "@services/auth.service";

import {HttpClientModule} from "@angular/common/http";

import {AuthModule} from "@auth0/auth0-angular";


import {from} from 'rxjs';
import {environment} from "../environments/environment";

@NgModule({
    declarations: [AppComponent],
    imports: [
        BrowserModule,
        IonicModule.forRoot(),
        HttpClientModule,
        AppRoutingModule,
        AuthModule.forRoot({
            domain: `${environment.auth0.url}.auth0.com`,
            clientId: environment.auth0.clientId
        })
    ],
    providers: [
        StatusBar,
        SplashScreen,
        AuthService,
        DrinksService,
        {provide: RouteReuseStrategy, useClass: IonicRouteStrategy}],
    bootstrap: [AppComponent],
})
export class AppModule {
}
