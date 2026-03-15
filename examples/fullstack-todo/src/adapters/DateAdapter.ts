// generated_from: behaviors/backend/crud
// spec_hash: 3bc5a2b2d95a1b99ae840d8085c5ad9eb0e9da675c885ce816b5d22fbee68c88
// generated_at: 2026-03-15T02:27:52.035770+00:00
// agent: implementation-agent
export class DateAdapter implements DateAdapter {
  nowIso(): string {
    return new Date().toISOString();
  }
}