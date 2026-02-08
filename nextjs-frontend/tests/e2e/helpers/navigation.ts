import { Page, expect } from '@playwright/test';

/**
 * Wait for the page to fully load past the loading skeleton state.
 * All pages in this app show an animate-pulse skeleton during data fetching.
 */
export async function waitForDataLoad(page: Page): Promise<void> {
  // Wait until the loading skeleton disappears
  await expect(page.locator('.animate-pulse').first()).toBeHidden({
    timeout: 15000,
  });
}

/**
 * Navigate to a page and wait for it to finish loading data.
 */
export async function navigateAndWaitForData(
  page: Page,
  path: string
): Promise<void> {
  await page.goto(path);
  await waitForDataLoad(page);
}

/**
 * Navigate using the sidebar link and wait for data to load.
 */
export async function navigateViaSidebar(
  page: Page,
  label: string
): Promise<void> {
  const sidebarLink = page.locator('aside nav a', { hasText: label });
  await sidebarLink.click();
  await waitForDataLoad(page);
}

/**
 * Select a region from the RegionFilter dropdown.
 * The RegionFilter uses a select element with id="region-filter".
 */
export async function selectRegion(
  page: Page,
  regionValue: string
): Promise<void> {
  await page.locator('#region-filter').selectOption(regionValue);
  // Wait for the data to reload after filter change
  await waitForDataLoad(page);
}

/**
 * Get the current page heading text (the h1 element).
 */
export async function getPageHeading(page: Page): Promise<string> {
  const heading = page.locator('h1').first();
  return (await heading.textContent()) ?? '';
}
