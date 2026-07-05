import { Component, OnInit, signal } from '@angular/core';
import { DatePipe } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { NseService } from '../../services/nse.service';
import { IndexDetail } from '../../models/nse.models';
import { fmt, signClass, toNum } from '../../shared/format.util';

@Component({
  selector: 'app-index-detail',
  imports: [RouterLink, DatePipe],
  templateUrl: './index-detail.component.html',
})
export class IndexDetailComponent implements OnInit {
  readonly fmt = fmt;
  readonly signClass = signClass;

  readonly index = signal<IndexDetail | null>(null);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);

  constructor(
    private route: ActivatedRoute,
    private nse: NseService,
  ) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe((params) => {
      const symbol = params.get('symbol');
      if (symbol) {
        this.load(symbol);
      }
    });
  }

  private load(symbol: string): void {
    this.loading.set(true);
    this.error.set(null);
    this.nse.getIndex(symbol).subscribe({
      next: (data) => {
        this.index.set(data);
        this.loading.set(false);
      },
      error: (err) => {
        const status = (err as { status?: number }).status;
        this.error.set(
          status === 404
            ? `Index "${symbol}" not found.`
            : 'Unable to load index details. Is the Django server running on http://localhost:8000?',
        );
        this.loading.set(false);
      },
    });
  }

  arrow(value: string | number | null): string {
    const n = toNum(value);
    if (n === null || n === 0) {
      return '—';
    }
    return n > 0 ? '▲' : '▼';
  }

  signStyle(value: string | number | null): string {
    const n = toNum(value);
    if (n === null || n === 0) {
      return '#6c757d';
    }
    return n > 0 ? '#28a745' : '#dc3545';
  }
}
