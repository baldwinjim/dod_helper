import { Component, inject, OnInit } from '@angular/core';
import { SpeakerService } from '../services/speaker-service';

@Component({
  selector: 'app-speakers',
  imports: [],
  templateUrl: './speakers.html',
  styleUrl: './speakers.scss',
})
export class Speakers implements OnInit {
  private _speakerService = inject(SpeakerService);

  ngOnInit(): void {
    this._speakerService.getSpeakersByYear(0).subscribe({
      next: (speakers) => {
        console.log('Speakers loaded:', speakers);
      },
    });
  }
}
