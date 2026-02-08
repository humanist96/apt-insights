import { test, expect } from '@playwright/test';
import { PriceTrendPage } from './pages/PriceTrendPage';
import {
  expectChartsVisible,
  expectStatsCardsVisible,
  expectNoErrorState,
  expectNoEmptyState,
  expectStatsCardWithTitle,
  expectTableWithRows,
} from './helpers/assertions';

test.describe('Price Trend Analysis Page', () => {
  let priceTrendPage: PriceTrendPage;

  test.beforeEach(async ({ page }) => {
    priceTrendPage = new PriceTrendPage(page);
    await priceTrendPage.goto();
  });

  test('should navigate to /price-trend and display page heading', async ({ page }) => {
    await expect(page).toHaveURL(/\/price-trend/);
    await priceTrendPage.expectLoaded();
  });

  test('should display all filter controls', async () => {
    await priceTrendPage.expectFiltersVisible();

    // Verify group-by options
    const monthOption = priceTrendPage.groupBySelect.locator('option[value="month"]');
    const quarterOption = priceTrendPage.groupBySelect.locator('option[value="quarter"]');
    await expect(monthOption).toBeAttached();
    await expect(quarterOption).toBeAttached();
  });

  test('should display summary stats cards', async ({ page }) => {
    await expectNoErrorState(page);
    await expectNoEmptyState(page);
    await expectStatsCardsVisible(page, 4);

    // Verify specific stats cards
    await expectStatsCardWithTitle(page, '총 기간');
    await expectStatsCardWithTitle(page, '전체 평균 가격');
    await expectStatsCardWithTitle(page, '가격 변동률');
    await expectStatsCardWithTitle(page, '총 거래 건수');
  });

  test('should render line chart for price trends', async ({ page }) => {
    await expectNoErrorState(page);
    await expectNoEmptyState(page);

    // Should render at least the main price trend line chart
    await expectChartsVisible(page);

    // Verify the line chart title
    const lineChartTitle = page.getByText('평균 거래가 추이');
    await expect(lineChartTitle).toBeVisible();
  });

  test('should render multiple charts (line, volume, combined)', async ({ page }) => {
    await expectNoErrorState(page);
    await expectNoEmptyState(page);

    // The page renders 3 charts: PriceTrendLineChart, TransactionVolumeChart, CombinedPriceVolumeChart
    const chartCount = await priceTrendPage.getChartCount();
    expect(chartCount).toBeGreaterThanOrEqual(3);
  });

  test('should display monthly statistics table', async ({ page }) => {
    await expectNoErrorState(page);
    await expectNoEmptyState(page);

    // Verify the table heading
    const tableTitle = page.getByText('월별 통계 테이블');
    await expect(tableTitle).toBeVisible();

    // Verify table has data rows
    const tableContainer = page.locator('table').first().locator('..');
    await expectTableWithRows(tableContainer, 1);
  });

  test('should display correct table headers', async ({ page }) => {
    await expectNoErrorState(page);

    const table = page.locator('table').first();
    await expect(table).toBeVisible();

    // Check column headers
    await expect(table.getByText('년월')).toBeVisible();
    await expect(table.getByText('평균 가격')).toBeVisible();
    await expect(table.getByText('중앙 가격')).toBeVisible();
    await expect(table.getByText('거래 건수')).toBeVisible();
    await expect(table.getByText('최고가')).toBeVisible();
    await expect(table.getByText('최저가')).toBeVisible();
  });

  test('should toggle group by from month to quarter', async ({ page }) => {
    await expectNoErrorState(page);

    // Default is "month"
    await expect(priceTrendPage.groupBySelect).toHaveValue('month');

    // Switch to quarter
    await priceTrendPage.setGroupBy('quarter');

    // Page should still load without errors
    await expectNoErrorState(page);

    // Verify the select value changed
    await expect(priceTrendPage.groupBySelect).toHaveValue('quarter');

    // Charts should still be visible
    const chartCount = await priceTrendPage.getChartCount();
    expect(chartCount).toBeGreaterThanOrEqual(1);
  });

  test('should handle date range input', async ({ page }) => {
    await expectNoErrorState(page);

    // Set a start date
    await priceTrendPage.startDateInput.fill('2024-01');
    await expect(priceTrendPage.startDateInput).toHaveValue('2024-01');

    // Set an end date
    await priceTrendPage.endDateInput.fill('2024-12');
    await expect(priceTrendPage.endDateInput).toHaveValue('2024-12');
  });

  test('should filter by region and maintain chart display', async ({ page }) => {
    await expectNoErrorState(page);
    await expectNoEmptyState(page);

    // Select a region
    await priceTrendPage.selectRegion('강남구');

    // Stats should still be visible
    await expectStatsCardsVisible(page, 4);

    // Charts should still render
    const chartCount = await priceTrendPage.getChartCount();
    expect(chartCount).toBeGreaterThanOrEqual(1);
  });

  test('summary metrics should show valid formatted values', async ({ page }) => {
    await expectNoErrorState(page);

    // Price values should contain the Korean unit
    const avgPriceValue = await expectStatsCardWithTitle(page, '전체 평균 가격');
    expect(avgPriceValue).toContain('억원');

    // Period should contain the unit
    const periodValue = await expectStatsCardWithTitle(page, '총 기간');
    expect(periodValue).toContain('개월');

    // Change rate should contain %
    const changeValue = await expectStatsCardWithTitle(page, '가격 변동률');
    expect(changeValue).toContain('%');
  });
});
