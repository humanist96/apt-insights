import { test, expect } from '@playwright/test';
import { InvestmentPage } from './pages/InvestmentPage';
import {
  expectChartsVisible,
  expectStatsCardsVisible,
  expectNoErrorState,
  expectStatsCardWithTitle,
  expectTableWithRows,
} from './helpers/assertions';

test.describe('Investment Analysis Page (Jeonse Ratio / Gap Investment)', () => {
  let investmentPage: InvestmentPage;

  test.beforeEach(async ({ page }) => {
    investmentPage = new InvestmentPage(page);
    await investmentPage.goto();
  });

  test('should navigate to /investment and display page heading', async ({ page }) => {
    await expect(page).toHaveURL(/\/investment/);
    await investmentPage.expectLoaded();
  });

  test('should display both analysis sections', async () => {
    await investmentPage.expectJeonseSectionVisible();
    await investmentPage.expectGapSectionVisible();
  });

  test('should display region filter and slider controls', async ({ page }) => {
    await expect(investmentPage.regionFilter).toBeVisible();
    await expect(investmentPage.jeonseRatioSlider).toBeVisible();
    await expect(investmentPage.gapRatioSlider).toBeVisible();

    // Verify slider labels
    await expect(investmentPage.jeonseRatioLabel).toBeVisible();
    await expect(investmentPage.gapRatioLabel).toBeVisible();
  });

  test('should display jeonse ratio stats cards', async ({ page }) => {
    await expectNoErrorState(page);
    await investmentPage.expectDataDisplayed();

    // Jeonse section stats
    await expectStatsCardWithTitle(page, '평균 전세가율');
    await expectStatsCardWithTitle(page, '중앙 전세가율');
    await expectStatsCardWithTitle(page, '매칭된 아파트');
  });

  test('should display risk summary cards (high, medium, low)', async () => {
    await investmentPage.expectRiskSummaryVisible();
  });

  test('should display gap investment stats cards', async ({ page }) => {
    await expectNoErrorState(page);

    // Gap section stats
    await expectStatsCardWithTitle(page, '평균 갭');
    await expectStatsCardWithTitle(page, '중앙 갭');
    await expectStatsCardWithTitle(page, '최소 갭');
    await expectStatsCardWithTitle(page, '분석 대상');
  });

  test('should render charts (jeonse ratio bar chart and scatter chart)', async ({ page }) => {
    await expectNoErrorState(page);

    // Should have at least the jeonse ratio chart and scatter chart
    await expectChartsVisible(page);
    const chartCount = await investmentPage.getChartCount();
    expect(chartCount).toBeGreaterThanOrEqual(2);
  });

  test('should display scatter chart with proper title and description', async ({ page }) => {
    const scatterTitle = page.getByText('매매가 vs 전세가 분포');
    await expect(scatterTitle).toBeVisible();

    const scatterDescription = page.getByText('버블 크기는 갭 금액을 나타냅니다');
    await expect(scatterDescription).toBeVisible();
  });

  test('should display high-risk apartment table', async ({ page }) => {
    const highRiskHeading = page.locator('h3', { hasText: '고위험 아파트 TOP 10' });
    await expect(highRiskHeading).toBeVisible();

    const tableContainer = highRiskHeading.locator('..');
    await expectTableWithRows(tableContainer, 1);

    // Check table columns
    const table = tableContainer.locator('table');
    await expect(table.getByText('아파트').first()).toBeVisible();
    await expect(table.getByText('지역').first()).toBeVisible();
    await expect(table.getByText('전세가율').first()).toBeVisible();
  });

  test('should display low-risk (investment opportunity) table', async ({ page }) => {
    const lowRiskHeading = page.locator('h3', { hasText: '저전세가율 아파트 TOP 10' });
    await expect(lowRiskHeading).toBeVisible();

    const tableContainer = lowRiskHeading.locator('..');
    await expectTableWithRows(tableContainer, 1);
  });

  test('should display gap investment recommendation table', async ({ page }) => {
    const gapHeading = page.locator('h3', { hasText: '갭투자 추천 물건' });
    await expect(gapHeading).toBeVisible();

    const tableContainer = gapHeading.locator('..').locator('..');
    await expectTableWithRows(tableContainer, 1);

    // Verify table columns specific to gap investment
    const table = tableContainer.locator('table');
    await expect(table.getByText('예상 ROI')).toBeVisible();
    await expect(table.getByText('갭 금액')).toBeVisible();
    await expect(table.getByText('갭 비율')).toBeVisible();
  });

  test('should adjust jeonse ratio slider and update label', async ({ page }) => {
    await expectNoErrorState(page);

    // Initial slider value should be 0
    await expect(investmentPage.jeonseRatioSlider).toHaveValue('0');
    await expect(investmentPage.jeonseRatioLabel).toContainText('0%');

    // Adjust the slider to 50
    await investmentPage.setJeonseRatioSlider(50);

    // The label should update to reflect new value
    await expect(investmentPage.jeonseRatioLabel).toContainText('50%');
  });

  test('should adjust gap ratio slider and update label', async ({ page }) => {
    await expectNoErrorState(page);

    // Initial slider value should be 0
    await expect(investmentPage.gapRatioSlider).toHaveValue('0');
    await expect(investmentPage.gapRatioLabel).toContainText('0%');

    // Adjust the slider to 20
    await investmentPage.setGapRatioSlider(20);

    // The label should update
    await expect(investmentPage.gapRatioLabel).toContainText('20%');
  });

  test('should filter by region and maintain data display', async ({ page }) => {
    await expectNoErrorState(page);

    // Select a specific region
    await investmentPage.selectRegion('강남구');

    // Page should still show data without errors
    await expectNoErrorState(page);
    await investmentPage.expectJeonseSectionVisible();
    await investmentPage.expectGapSectionVisible();
  });

  test('jeonse ratio stats should show percentage values', async ({ page }) => {
    await expectNoErrorState(page);

    const avgRatioValue = await expectStatsCardWithTitle(page, '평균 전세가율');
    expect(avgRatioValue).toContain('%');

    const medianRatioValue = await expectStatsCardWithTitle(page, '중앙 전세가율');
    expect(medianRatioValue).toContain('%');
  });

  test('gap stats should show Korean currency units', async ({ page }) => {
    await expectNoErrorState(page);

    const avgGapValue = await expectStatsCardWithTitle(page, '평균 갭');
    expect(avgGapValue).toContain('억원');

    const medianGapValue = await expectStatsCardWithTitle(page, '중앙 갭');
    expect(medianGapValue).toContain('억원');
  });
});
