import { Page, Locator, expect } from '@playwright/test';

/**
 * Assert that Recharts-based chart containers are visible on the page.
 * Recharts renders inside a <div> with a ResponsiveContainer that
 * produces an <svg> element with class "recharts-surface".
 */
export async function expectChartsVisible(
  page: Page,
  expectedCount?: number
): Promise<void> {
  const charts = page.locator('.recharts-surface');
  if (expectedCount !== undefined) {
    await expect(charts).toHaveCount(expectedCount);
  } else {
    await expect(charts.first()).toBeVisible();
  }
}

/**
 * Assert that StatsCard components are rendered with values.
 * StatsCards render as cards with a title (h3) and a bold value (p.text-2xl).
 */
export async function expectStatsCardsVisible(
  page: Page,
  expectedMinimum: number
): Promise<void> {
  const statsValues = page.locator('p.text-2xl.font-bold');
  const count = await statsValues.count();
  expect(count).toBeGreaterThanOrEqual(expectedMinimum);
}

/**
 * Assert that a stats card with a specific title exists and has a non-empty value.
 */
export async function expectStatsCardWithTitle(
  page: Page,
  title: string
): Promise<string> {
  const card = page.locator('h3.text-sm.font-medium', { hasText: title }).locator('..');
  await expect(card).toBeVisible();
  const valueEl = card.locator('p.text-2xl.font-bold');
  await expect(valueEl).toBeVisible();
  const value = await valueEl.textContent();
  expect(value).toBeTruthy();
  return value ?? '';
}

/**
 * Assert that a data table is visible and has at least a minimum number of rows.
 */
export async function expectTableWithRows(
  container: Locator,
  minRows: number
): Promise<void> {
  const table = container.locator('table').first();
  await expect(table).toBeVisible();
  const bodyRows = table.locator('tbody tr');
  const count = await bodyRows.count();
  expect(count).toBeGreaterThanOrEqual(minRows);
}

/**
 * Assert that an error state is NOT shown (no red error banner).
 */
export async function expectNoErrorState(page: Page): Promise<void> {
  const errorBanner = page.locator('.bg-red-50, .bg-red-900\\/20');
  await expect(errorBanner).toHaveCount(0);
}

/**
 * Assert that the empty data state is NOT shown.
 */
export async function expectNoEmptyState(page: Page): Promise<void> {
  const emptyText = page.getByText('표시할 데이터가 없습니다');
  await expect(emptyText).toHaveCount(0);
}

/**
 * Assert that a select element contains specific option values.
 */
export async function expectSelectOptions(
  locator: Locator,
  expectedValues: string[]
): Promise<void> {
  for (const val of expectedValues) {
    const option = locator.locator(`option[value="${val}"]`);
    await expect(option).toBeAttached();
  }
}
