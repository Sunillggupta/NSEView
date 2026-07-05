import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { environment } from '../../environments/environment';
import {
  ApiStatus,
  HealthStatus,
  IndexDetail,
  IndexHistory,
  IndexListItem,
  Paginated,
  RefreshResult,
} from '../models/nse.models';

/**
 * Single point of contact with the Django REST API.
 */
@Injectable({ providedIn: 'root' })
export class NseService {
  private readonly base = environment.apiUrl;

  constructor(private http: HttpClient) {}

  /** Fetch every index in one request (page_size override) for the dashboard. */
  getAllIndices(search?: string, ordering?: string): Observable<IndexListItem[]> {
    let params = new HttpParams().set('page_size', '500');
    if (search) {
      params = params.set('search', search);
    }
    if (ordering) {
      params = params.set('ordering', ordering);
    }
    return this.http
      .get<Paginated<IndexListItem>>(`${this.base}/indices/`, { params })
      .pipe(map((res) => res.results));
  }

  /** Retrieve a single index by its symbol. */
  getIndex(symbol: string): Observable<IndexDetail> {
    return this.http.get<IndexDetail>(
      `${this.base}/indices/${encodeURIComponent(symbol)}/`,
    );
  }

  /** Historical snapshots for one index. */
  getIndexHistory(symbol: string): Observable<IndexHistory[]> {
    return this.http.get<IndexHistory[]>(
      `${this.base}/indices/${encodeURIComponent(symbol)}/history/`,
    );
  }

  /** Trigger a fresh pull from NSE into the backend database. */
  refreshIndices(): Observable<RefreshResult> {
    return this.http.get<RefreshResult>(`${this.base}/indices/refresh/`);
  }

  getApiStatus(): Observable<ApiStatus> {
    return this.http.get<ApiStatus>(`${this.base}/status/status/`);
  }

  getHealth(): Observable<HealthStatus> {
    return this.http.get<HealthStatus>(`${this.base}/status/health/`);
  }
}
