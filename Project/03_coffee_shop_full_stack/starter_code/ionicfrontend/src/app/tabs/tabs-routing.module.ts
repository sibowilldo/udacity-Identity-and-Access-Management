import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TabsPage } from './tabs.page';

const routes: Routes = [
  {
    path: 'tabs',
    component: TabsPage,
    children: [
      {
        path: 'drink-menu',
        loadChildren: () => import('../pages/drink-menu/drink-menu.module').then( m => m.DrinkMenuPageModule)
      },
      {
        path: 'user-page',
        loadChildren: () => import('../pages/user-page/user-page.module').then( m => m.UserPagePageModule)
      },
      {
        path: '',
        redirectTo: '/tabs/drink-menu',
        pathMatch: 'full'
      }
    ]
  },
  {
    path: '',
    redirectTo: '/tabs/drink-menu',
    pathMatch: 'full'
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TabsPageRoutingModule {}
