import { Component, OnInit, signal } from '@angular/core';
import { KeyValuePipe } from '@angular/common';

import { NseService } from '../../services/nse.service';
import { ApiStatus, HealthStatus } from '../../models/nse.models';

@Component({
  selector: 'app-status',
  imports: [KeyValuePipe],
  templateUrl: './status.component.html',
})
export class StatusComponent implements OnInit {
  readonly status = signal<ApiStatus | null>(null);
  readonly health = signal<HealthStatus | null>(null);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);

  constructor(private nse: NseService) {}

  ngOnInit(): void {
    this.reload();
  }

  reload(): void {
    this.loading.set(true);
    this.error.set(null);

    this.nse.getHealth().subscribe({
      next: (h) => this.health.set(h),
      error: () => this.health.set(null),
    });

    this.nse.getApiStatus().subscribe({
      next: (s) => {
        this.status.set(s);
        this.loading.set(false);
      },
      error: () => {
        this.error.set(
          'Cannot reach the API. Ensure the Django server is running on http://localhost:8000.',
        );
        this.loading.set(false);
      },
    });
  }
}
