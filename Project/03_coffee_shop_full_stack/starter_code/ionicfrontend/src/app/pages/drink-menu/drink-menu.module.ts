import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { DrinkMenuPageRoutingModule } from './drink-menu-routing.module';

import { DrinkMenuPage } from './drink-menu.page';
import { DrinkFormComponent } from './drink-form/drink-form.component';
import { DrinkGraphicComponent } from './drink-graphic/drink-graphic.component';


@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        IonicModule,
        DrinkMenuPageRoutingModule,

    ],
  entryComponents: [DrinkFormComponent],
  declarations: [DrinkMenuPage, DrinkGraphicComponent, DrinkFormComponent]
})
export class DrinkMenuPageModule {}
