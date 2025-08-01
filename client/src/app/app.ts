import { Component, signal } from '@angular/core';

import { Header } from './header/header';
import { Sidebar } from './sidebar/sidebar';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [Header, Sidebar, RouterModule],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  protected readonly title = signal('devopsdays_helper');
}
