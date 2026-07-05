/**
 * TypeScript interfaces mirroring the Django REST API payloads.
 */

/** Row shape returned by GET /api/indices/ (list). */
export interface IndexListItem {
  id: number;
  name: string;
  symbol: string;
  key: string;
  last_price: string | null;
  change: string | null;
  percent_change: string | null;
  open_price: string | null;
  high_price: string | null;
  low_price: string | null;
  previous_close: string | null;
  pe_ratio: string | null;
}

/** Historical snapshot returned inside index detail / history endpoints. */
export interface IndexHistory {
  id: number;
  index: number;
  index_name: string;
  timestamp: string;
  price: string;
  change: string | null;
  percent_change: string | null;
}

/** Full shape returned by GET /api/indices/{symbol}/ (retrieve). */
export interface IndexDetail extends IndexListItem {
  year_high: string | null;
  year_low: string | null;
  pb_ratio: string | null;
  dividend_yield: string | null;
  advances: number | null;
  declines: number | null;
  unchanged: number | null;
  change_30d: string | null;
  change_365d: string | null;
  last_updated: string;
  created_at: string;
  history: IndexHistory[];
}

/** Generic DRF paginated envelope. */
export interface Paginated<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface RefreshResult {
  status: string;
  message: string;
  created: number;
  updated: number;
  total: number;
  timestamp: string | null;
}

export interface ApiStatus {
  status: string;
  message: string;
  endpoints?: Record<string, string>;
  available_indices?: number;
  timestamp?: string | null;
  note?: string;
}

export interface HealthStatus {
  status: string;
  database: string;
  api: string;
}
