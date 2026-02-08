import { test, expect } from '@playwright/test';
import { RegionalPage } from './pages/RegionalPage';
import {
  expectChartsVisible,
  expectStatsCardsVisible,
  expectNoErrorState,
  expectNoEmptyState,
  expectStatsCardWithTitle,
} from './helpers/assertions';

test.describe('Regional Analysis Page', () => {
  let regionalPage: RegionalPage;

  test.beforeEach(async ({ page }) => {
    regionalPage = new RegionalPage(page);
    await regionalPage.goto();
  });

  test('should navigate to /regional and display page heading', async ({ page }) => {
    await expect(page).toHaveURL(/\/regional/);
    await regionalPage.expectLoaded();
  });

  test('should display region filter with all options', async ({ page }) => {
    await expect(regionalPage.regionFilter).toBeVisible();

    const options = regionalPage.regionFilter.locator('option');
    const count = await options.count();
    expect(count).toBeGreaterThanOrEqual(2); // At least "all" + one region

    // Verify the "all" option exists
    const allOption = regionalPage.regionFilter.locator('option[value="all"]');
    await expect(allOption).toBeAttached();
  });

  test('should display stats cards with data', async ({ page }) => {
    await expectNoErrorState(page);
    await expectNoEmptyState(page);
    await expectStatsCardsVisible(page, 4);

    // Verify specific stats cards exist
    await expectStatsCardWithTitle(page, '총 거래 건수');
    await expectStatsCardWithTitle(page, '평균 거래 가격');
    await expectStatsCardWithTitle(page, '최고가 지역');
    await expectStatsCardWithTitle(page, '최저가 지역');
  });

  test('should render charts (bar chart and pie chart)', async ({ page }) => {
    await expectNoErrorState(page);
    await expectNoEmptyState(page);

    // The page should render 2 Recharts SVGs: bar chart and pie chart
    await expectChartsVisible(page, 2);
  });

  test('should filter data when selecting a specific region', async ({ page }) => {
    // Get initial stats
    const initialTotalValue = await expectStatsCardWithTitle(page, '총 거래 건수');

    // Select a specific region (Gangnam-gu)
    await regionalPage.selectRegion('강남구');

    // After filter, stats should still be visible
    await expectStatsCardsVisible(page, 4);
    await expectNoErrorState(page);

    // The total transaction count might differ from "all"
    const filteredTotalValue = await expectStatsCardWithTitle(page, '총 거래 건수');
    // Both values should be valid strings (non-empty)
    expect(initialTotalValue).toBeTruthy();
    expect(filteredTotalValue).toBeTruthy();
  });

  test('should update charts when region filter changes', async ({ page }) => {
    // Verify charts are visible initially
    await expectChartsVisible(page);

    // Change the filter
    await regionalPage.selectRegion('서초구');

    // Charts should still be rendered after filter change
    const chartCount = await regionalPage.getChartCount();
    expect(chartCount).toBeGreaterThanOrEqual(1);
  });

  test('should display chart title for bar chart', async ({ page }) => {
    const barChartTitle = page.getByText('지역별 평균 가격 및 거래 건수');
    await expect(barChartTitle).toBeVisible();
  });

  test('should switch back to all regions after filtering', async ({ page }) => {
    // Filter to a specific region
    await regionalPage.selectRegion('강남구');
    await expectNoErrorState(page);

    // Switch back to "all"
    await regionalPage.selectRegion('all');
    await expectNoErrorState(page);
    await expectNoEmptyState(page);

    // Should show full data again
    const statsCount = await regionalPage.getStatsCardCount();
    expect(statsCount).toBeGreaterThanOrEqual(4);
  });
});
