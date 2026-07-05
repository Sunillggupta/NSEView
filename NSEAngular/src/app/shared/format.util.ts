/**
 * Small formatting helpers shared across views. The API returns numeric
 * fields as strings (DRF DecimalField), so these tolerate string | number | null.
 */

export function toNum(value: string | number | null | undefined): number | null {
  if (value === null || value === undefined || value === '') {
    return null;
  }
  const n = typeof value === 'number' ? value : parseFloat(value);
  return Number.isNaN(n) ? null : n;
}

/** Fixed-2 formatting with an 'N/A' fallback, mirroring the Jinja templates. */
export function fmt(value: string | number | null | undefined, digits = 2): string {
  const n = toNum(value);
  return n === null ? 'N/A' : n.toFixed(digits);
}

/** CSS class for a signed value: positive / negative / neutral. */
export function signClass(value: string | number | null | undefined): string {
  const n = toNum(value);
  if (n === null || n === 0) {
    return 'neutral';
  }
  return n > 0 ? 'positive' : 'negative';
}
