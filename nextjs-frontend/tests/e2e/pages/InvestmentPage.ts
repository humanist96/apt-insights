import { Page, Locator, expect } from '@playwright/test';
import { waitForDataLoad } from '../helpers/navigation';

export class InvestmentPage {
  readonly page: Page;
  readonly heading: Locator;
  readonly subtitle: Locator;
  readonly regionFilter: Locator;
  readonly jeonseRatioSlider: Locator;
  readonly jeonseRatioLabel: Locator;
  readonly gapRatioSlider: Locator;
  readonly gapRatioLabel: Locator;
  readonly statsCards: Locator;
  readonly chartContainers: Locator;
  readonly jeonseSection: Locator;
  readonly gapSection: Locator;
  readonly highRiskTable: Locator;
  readonly lowRiskTable: Locator;
  readonly gapRecommendationTable: Locator;
  readonly riskCards: Locator;
  readonly scatterChart: Locator;
  readonly loadingSkeleton: Locator;
  readonly errorBanner: Locator;
  readonly emptyState: Locator;

  constructor(page: Page) {
    this.page = page;
    this.heading = page.locator('h1', { hasText: '전세가율/갭투자 분석' });
    this.subtitle = page.getByText('전세가율과 갭투자 기회를 분석합니다');
    this.regionFilter = page.locator('#region-filter');
    this.jeonseRatioSlider = page.locator('input[type="range"]').first();
    this.jeonseRatioLabel = page.getByText(/최소 전세가율:/);
    this.gapRatioSlider = page.locator('input[type="range"]').nth(1);
    this.gapRatioLabel = page.getByText(/최소 갭 비율:/);
    this.statsCards = page.locator('p.text-2xl.font-bold');
    this.chartContainers = page.locator('.recharts-surface');
    this.jeonseSection = page.locator('section').first();
    this.gapSection = page.locator('section').nth(1);
    this.highRiskTable = page.locator('h3', { hasText: '고위험 아파트 TOP 10' }).locator('..').locator('table');
    this.lowRiskTable = page.locator('h3', { hasText: '저전세가율 아파트 TOP 10' }).locator('..').locator('table');
    this.gapRecommendationTable = page.locator('h3', { hasText: '갭투자 추천 물건' }).locator('..').locator('table');
    this.riskCards = page.locator('.bg-red-50, .bg-yellow-50, .bg-green-50');
    this.scatterChart = page.locator('.recharts-scatter');
    this.loadingSkeleton = page.locator('.animate-pulse').first();
    this.errorBanner = page.locator('.bg-red-50').first();
    this.emptyState = page.getByText('표시할 데이터가 없습니다');
  }

  async goto(): Promise<void> {
    await this.page.goto('/investment');
    await waitForDataLoad(this.page);
  }

  async selectRegion(regionValue: string): Promise<void> {
    await this.regionFilter.selectOption(regionValue);
    await waitForDataLoad(this.page);
  }

  async setJeonseRatioSlider(value: number): Promise<void> {
    await this.jeonseRatioSlider.fill(String(value));
    await waitForDataLoad(this.page);
  }

  async setGapRatioSlider(value: number): Promise<void> {
    await this.gapRatioSlider.fill(String(value));
    await waitForDataLoad(this.page);
  }

  async getStatsCardCount(): Promise<number> {
    return await this.statsCards.count();
  }

  async getChartCount(): Promise<number> {
    return await this.chartContainers.count();
  }

  async expectLoaded(): Promise<void> {
    await expect(this.heading).toBeVisible();
    await expect(this.subtitle).toBeVisible();
  }

  async expectJeonseSectionVisible(): Promise<void> {
    const sectionHeading = this.page.locator('h2', { hasText: '전세가율 분석' });
    await expect(sectionHeading).toBeVisible();
  }

  async expectGapSectionVisible(): Promise<void> {
    const sectionHeading = this.page.locator('h2', { hasText: '갭투자 분석' });
    await expect(sectionHeading).toBeVisible();
  }

  async expectRiskSummaryVisible(): Promise<void> {
    await expect(this.page.getByText('위험 (80% 이상)')).toBeVisible();
    await expect(this.page.getByText('주의 (70-80%)')).toBeVisible();
    await expect(this.page.getByText('안전 (70% 미만)')).toBeVisible();
  }

  async expectDataDisplayed(): Promise<void> {
    await expect(this.emptyState).toHaveCount(0);
    const statsCount = await this.getStatsCardCount();
    expect(statsCount).toBeGreaterThanOrEqual(4);
  }
}
