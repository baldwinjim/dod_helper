import { inject, Injectable } from '@angular/core';
import { delay, Observable, of } from 'rxjs';
import { Speaker, Sponsor } from '../models/models';
import { MockDataService } from './mock-data-service';

@Injectable({
  providedIn: 'root',
})
export class SpeakerService {
  private _mockDataService = inject(MockDataService);

  public getSpeakersByYear(year: number): Observable<Speaker[]> {
    return of(this._mockDataService.speakers).pipe(delay(1000));
  }

  public getSponsorsByYear(year: number): Observable<Sponsor[]> {
    return of(this._mockDataService.sponsors);
  }
}
