import { Page, Locator, expect } from '@playwright/test';
import { waitForDataLoad } from '../helpers/navigation';

export class RegionalPage {
  readonly page: Page;
  readonly heading: Locator;
  readonly subtitle: Locator;
  readonly regionFilter: Locator;
  readonly statsCards: Locator;
  readonly chartContainers: Locator;
  readonly barChart: Locator;
  readonly pieChart: Locator;
  readonly loadingSkeleton: Locator;
  readonly errorBanner: Locator;
  readonly emptyState: Locator;

  constructor(page: Page) {
    this.page = page;
    this.heading = page.locator('h1', { hasText: '지역별 분석' });
    this.subtitle = page.getByText('지역별 아파트 거래 현황을 분석합니다');
    this.regionFilter = page.locator('#region-filter');
    this.statsCards = page.locator('p.text-2xl.font-bold');
    this.chartContainers = page.locator('.recharts-surface');
    this.barChart = page.locator('.recharts-bar');
    this.pieChart = page.locator('.recharts-pie');
    this.loadingSkeleton = page.locator('.animate-pulse').first();
    this.errorBanner = page.locator('.bg-red-50');
    this.emptyState = page.getByText('표시할 데이터가 없습니다');
  }

  async goto(): Promise<void> {
    await this.page.goto('/regional');
    await waitForDataLoad(this.page);
  }

  async selectRegion(regionValue: string): Promise<void> {
    await this.regionFilter.selectOption(regionValue);
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
    await expect(this.errorBanner).toHaveCount(0);
  }

  async expectDataDisplayed(): Promise<void> {
    await expect(this.emptyState).toHaveCount(0);
    const statsCount = await this.getStatsCardCount();
    expect(statsCount).toBeGreaterThanOrEqual(4);
    const chartCount = await this.getChartCount();
    expect(chartCount).toBeGreaterThanOrEqual(1);
  }
}
