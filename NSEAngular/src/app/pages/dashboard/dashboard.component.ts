import { Component, OnInit, computed, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { NseService } from '../../services/nse.service';
import { IndexListItem } from '../../models/nse.models';
import { fmt, signClass, toNum } from '../../shared/format.util';

type FilterType = 'all' | 'derivative' | 'broad';

@Component({
  selector: 'app-dashboard',
  imports: [RouterLink],
  templateUrl: './dashboard.component.html',
})
export class DashboardComponent implements OnInit {
  // Expose formatting helpers to the template.
  readonly fmt = fmt;
  readonly signClass = signClass;

  private readonly all = signal<IndexListItem[]>([]);
  readonly search = signal('');
  readonly filter = signal<FilterType>('all');

  readonly loading = signal(false);
  readonly error = signal<string | null>(null);
  readonly refreshing = signal(false);
  readonly refreshMessage = signal<string | null>(null);

  readonly total = computed(() => this.all().length);

  /** Client-side search + category filter, matching the original Flask UX. */
  readonly visible = computed(() => {
    const term = this.search().trim().toLowerCase();
    const type = this.filter();
    return this.all().filter((idx) => {
      const matchesSearch = !term || idx.name.toLowerCase().includes(term);
      const matchesType = type === 'all' || this.categoryOf(idx) === type;
      return matchesSearch && matchesType;
    });
  });

  constructor(private nse: NseService) {}

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.loading.set(true);
    this.error.set(null);
    this.nse.getAllIndices(undefined, 'name').subscribe({
      next: (data) => {
        this.all.set(data);
        this.loading.set(false);
      },
      error: (err) => {
        this.error.set(this.describe(err));
        this.loading.set(false);
      },
    });
  }

  refresh(): void {
    this.refreshing.set(true);
    this.refreshMessage.set(null);
    this.error.set(null);
    this.nse.refreshIndices().subscribe({
      next: (res) => {
        this.refreshMessage.set(res.message);
        this.refreshing.set(false);
        this.load();
      },
      error: (err) => {
        this.error.set(this.describe(err));
        this.refreshing.set(false);
      },
    });
  }

  setFilter(type: FilterType): void {
    this.filter.set(type);
  }

  onSearch(event: Event): void {
    this.search.set((event.target as HTMLInputElement).value);
  }

  categoryOf(idx: IndexListItem): FilterType | 'other' {
    const key = (idx.key || '').toUpperCase();
    if (key.includes('DERIVATIVES')) {
      return 'derivative';
    }
    if (key.includes('BROAD')) {
      return 'broad';
    }
    return 'other';
  }

  private describe(err: unknown): string {
    const e = err as { status?: number; message?: string };
    if (e?.status === 0) {
      return 'Cannot reach the API. Is the Django server running on http://localhost:8000?';
    }
    return e?.message || 'An unexpected error occurred while loading indices.';
  }

  // Helpers for the arrow glyphs used in the change columns.
  arrow(value: string | number | null): string {
    const n = toNum(value);
    if (n === null || n === 0) {
      return '—';
    }
    return n > 0 ? '▲' : '▼';
  }
}
