export interface RegionalDataItem {
  region: string;
  count: number;
  avg_price: number;
  total: number;
}

export interface RegionalSummary {
  total_transactions: number;
  average_price: number;
  total_volume: number;
  highest_region?: {
    region: string;
    avg_price: number;
  };
  lowest_region?: {
    region: string;
    avg_price: number;
  };
}

export interface RegionalAnalysis {
  by_region: RegionalDataItem[];
  summary: RegionalSummary;
}

export interface ApartmentDataItem {
  apt_name: string;
  region?: string;
  count: number;
  avg_price?: number;
  max_price?: number;
  min_price?: number;
  avg_price_per_area?: number;
  build_year?: string;
  floor_range?: string;
  deals?: Array<{
    deal_date: string;
    price: number;
    area: number;
    floor: string;
    price_per_area: number;
  }>;
}

export interface ApartmentDetail {
  found: boolean;
  apt_name: string;
  overall?: {
    total_count: number;
    avg_price: number;
    avg_price_per_area: number;
    build_year: string;
    min_price: number;
    max_price: number;
  };
  by_area?: Array<{
    area: number;
    count: number;
    avg_price: number;
    max_price: number;
    min_price: number;
    avg_price_per_area: number;
  }>;
}

export interface ApartmentAnalysis {
  data: ApartmentDataItem[];
}

export interface PriceTrendDataItem {
  year_month: string;
  avg_price: number;
  median_price: number;
  count: number;
  max_price: number;
  min_price: number;
}

export interface PriceTrendSummary {
  total_months: number;
  overall_avg_price: number;
  price_change_pct: number;
  highest_month?: {
    year_month: string;
    avg_price: number;
  };
  lowest_month?: {
    year_month: string;
    avg_price: number;
  };
  total_transactions: number;
}

export interface PriceTrendAnalysis {
  trend_data: PriceTrendDataItem[];
  summary: PriceTrendSummary;
}

export interface JeonseRatioDataItem {
  region: string;
  avg_jeonse_ratio: number;
  avg_gap: number;
  count: number;
}

export interface JeonseRatioApartment {
  apt_name: string;
  region: string;
  jeonse_ratio: number;
  avg_trade_price: number;
  avg_jeonse_price: number;
  gap: number;
}

export interface JeonseRatioAnalysis {
  by_region: JeonseRatioDataItem[];
  high_ratio_apartments: JeonseRatioApartment[];
  low_ratio_apartments: JeonseRatioApartment[];
  jeonse_stats: {
    avg_jeonse_ratio: number;
    median_jeonse_ratio: number;
    avg_gap: number;
    matched_apartments: number;
  };
  risk_summary: {
    high_risk_count: number;
    medium_risk_count: number;
    low_risk_count: number;
  };
}

export interface GapInvestmentOpportunity {
  apt_name: string;
  region: string;
  gap: number;
  gap_ratio: number;
  avg_trade_price: number;
  avg_jeonse_price: number;
  jeonse_ratio: number;
  estimated_roi?: number;
}

export interface GapInvestmentAnalysis {
  opportunities: GapInvestmentOpportunity[];
  gap_stats: {
    avg_gap: number;
    median_gap: number;
    min_gap: number;
    total_count: number;
  };
  by_gap_range: Array<{
    gap_range: string;
    count: number;
    avg_jeonse_ratio: number;
  }>;
}

export interface AreaAnalysisDataItem {
  area_range: string;
  count: number;
  avg_price: number;
  median_price: number;
  max_price?: number;
  min_price?: number;
  avg_area: number;
  price_per_area: number;
}

export interface AreaAnalysisSummary {
  total_transactions: number;
  most_common_range?: {
    area_range: string;
    count: number;
  };
}

export interface AreaAnalysis {
  data: AreaAnalysisDataItem[];
  summary: AreaAnalysisSummary;
  bins: number[];
}

export interface PricePerAreaDataItem {
  apt_name: string;
  region: string;
  price_per_area: number;
  total_price: number;
  area: number;
  floor?: number;
  build_year?: number;
  deal_date: string;
}

export interface PricePerAreaByRegion {
  region: string;
  count: number;
  avg_price_per_area: number;
  median_price_per_area: number;
  max_price_per_area: number;
  min_price_per_area: number;
}

export interface PricePerAreaByAreaRange {
  area_range: string;
  count: number;
  avg_price_per_area: number;
  median_price_per_area: number;
  avg_total_price: number;
  avg_area: number;
}

export interface PricePerAreaByBuildYear {
  build_year_range: string;
  count: number;
  avg_price_per_area: number;
  median_price_per_area: number;
  avg_build_year: number;
}

export interface PricePerAreaStats {
  avg_price_per_area: number;
  median_price_per_area: number;
  max_price_per_area: number;
  min_price_per_area: number;
  std_price_per_area: number;
  total_count: number;
}

export interface PricePerAreaAnalysis {
  stats: PricePerAreaStats;
  by_region: PricePerAreaByRegion[];
  by_area_range: PricePerAreaByAreaRange[];
  by_build_year: PricePerAreaByBuildYear[];
  top_expensive: PricePerAreaDataItem[];
  top_affordable: PricePerAreaDataItem[];
}

export interface PricePerAreaTrendItem {
  year_month: string;
  count: number;
  avg_price_per_area: number;
  median_price_per_area: number;
  max_price_per_area: number;
  min_price_per_area: number;
  change_rate?: number;
}

export interface PricePerAreaTrendAnalysis {
  trend: PricePerAreaTrendItem[];
}

export interface BargainSalesItem {
  apt_name: string;
  region: string;
  area_group: number;
  current_price: number;
  avg_price: number;
  discount_pct: number;
  deal_date: string;
  floor: number;
  area: number;
  savings: number;
}

export interface BargainSalesRegion {
  region: string;
  bargain_count: number;
  total_count: number;
  bargain_rate: number;
}

export interface BargainSalesAnalysis {
  bargain_items: BargainSalesItem[];
  stats: {
    total_trades: number;
    compared_trades: number;
    bargain_count: number;
    bargain_rate: number;
    avg_discount: number;
    max_discount: number;
    total_savings: number;
    threshold_pct: number;
  };
  by_region: BargainSalesRegion[];
}

export interface DetailDataItem {
  id: string;
  apt_name: string;
  region: string;
  deal_amount: number;
  area: number;
  floor: number;
  build_year: number;
  deal_date: string;
  transaction_type: string;
  api_type: string;
}

export interface DetailDataFilters {
  regions: string[];
  dateStart?: string;
  dateEnd?: string;
  priceMin?: number;
  priceMax?: number;
  areaMin?: number;
  areaMax?: number;
  floorMin?: number;
  floorMax?: number;
  transactionTypes: string[];
  searchQuery?: string;
}

export interface DetailDataResponse {
  items: DetailDataItem[];
  total_count: number;
}

export interface RentVsJeonseStats {
  total_count: number;
  jeonse_count: number;
  wolse_count: number;
  jeonse_ratio: number;
  wolse_ratio: number;
  avg_conversion_rate: number;
  median_conversion_rate: number;
  min_conversion_rate?: number;
  max_conversion_rate?: number;
}

export interface RentVsJeonseRegion {
  region: string;
  jeonse_count: number;
  wolse_count: number;
  total_count: number;
  jeonse_ratio: number;
  wolse_ratio: number;
  avg_conversion_rate: number;
}

export interface RentVsJeonseArea {
  area_range: string;
  jeonse_count: number;
  wolse_count: number;
  total_count: number;
  jeonse_ratio: number;
  wolse_ratio: number;
  avg_conversion_rate: number;
}

export interface RentVsJeonseFloor {
  floor_category: string;
  jeonse_count: number;
  wolse_count: number;
  total_count: number;
  jeonse_ratio: number;
  wolse_ratio: number;
}

export interface RentVsJeonseDeposit {
  deposit_range: string;
  count: number;
  avg_conversion_rate: number;
  median_conversion_rate: number;
  avg_monthly_rent: number;
  avg_deposit: number;
}

export interface RentVsJeonseTrend {
  year_month: string;
  jeonse_count: number;
  wolse_count: number;
  total_count: number;
  jeonse_ratio: number;
  wolse_ratio: number;
  avg_conversion_rate: number;
}

export interface RentVsJeonseAnalysis {
  has_data: boolean;
  message?: string;
  stats: RentVsJeonseStats;
  by_region: RentVsJeonseRegion[];
  by_area: RentVsJeonseArea[];
  by_floor: RentVsJeonseFloor[];
  by_deposit: RentVsJeonseDeposit[];
  trend?: RentVsJeonseTrend[];
}

export interface DealingTypeStats {
  total_count: number;
  broker_count: number;
  direct_count: number;
  other_count: number;
  broker_ratio: number;
  direct_ratio: number;
  broker_avg_price: number;
  broker_median_price: number;
  direct_avg_price: number;
  direct_median_price: number;
  price_diff: number;
  price_diff_pct: number;
}

export interface DealingTypeRegion {
  region: string;
  broker_count: number;
  direct_count: number;
  total_count: number;
  direct_ratio: number;
  broker_avg_price: number;
  direct_avg_price: number;
}

export interface DealingTypePriceRange {
  price_range: string;
  broker_count: number;
  direct_count: number;
  total_count: number;
  broker_ratio: number;
  direct_ratio: number;
}

export interface DealingTypeMonth {
  year_month: string;
  broker_count: number;
  direct_count: number;
  total_count: number;
  direct_ratio: number;
}

export interface DealingTypeAnalysis {
  has_data: boolean;
  message?: string;
  stats: DealingTypeStats;
  by_region: DealingTypeRegion[];
  by_price_range: DealingTypePriceRange[];
  by_month: DealingTypeMonth[];
}

export interface BuyerSellerStats {
  total_count: number;
  buyer_types: Record<string, number>;
  seller_types: Record<string, number>;
  buyer_법인_count: number;
  buyer_법인_ratio: number;
  buyer_법인_avg_price: number;
  buyer_개인_count: number;
  buyer_개인_ratio: number;
  buyer_개인_avg_price: number;
  buyer_미공개_count: number;
  buyer_미공개_ratio: number;
  buyer_미공개_avg_price: number;
  seller_법인_count: number;
  seller_법인_ratio: number;
  seller_법인_avg_price: number;
  seller_개인_count: number;
  seller_개인_ratio: number;
  seller_개인_avg_price: number;
  seller_미공개_count: number;
  seller_미공개_ratio: number;
  seller_미공개_avg_price: number;
}

export interface BuyerSellerRegion {
  region: string;
  total_count: number;
  buyer_법인_count: number;
  buyer_법인_ratio: number;
  seller_법인_count: number;
  seller_법인_ratio: number;
}

export interface BuyerSellerMonth {
  year_month: string;
  total_count: number;
  buyer_법인_count: number;
  buyer_법인_ratio: number;
  seller_법인_count: number;
  seller_법인_ratio: number;
}

export interface BuyerSellerAnalysis {
  has_data: boolean;
  message?: string;
  stats: BuyerSellerStats;
  by_region: BuyerSellerRegion[];
  by_month: BuyerSellerMonth[];
}

export interface CancelledDealsStats {
  total_count: number;
  cancelled_count: number;
  normal_count: number;
  cancel_ratio: number;
  cancel_types: Record<string, number>;
  cancelled_avg_price: number;
  normal_avg_price: number;
}

export interface CancelledDealsRegion {
  region: string;
  cancelled_count: number;
  normal_count: number;
  total_count: number;
  cancel_ratio: number;
}

export interface CancelledDealsPriceRange {
  price_range: string;
  cancelled_count: number;
  normal_count: number;
  total_count: number;
  cancel_ratio: number;
}

export interface CancelledDealsMonth {
  year_month: string;
  cancelled_count: number;
  normal_count: number;
  total_count: number;
  cancel_ratio: number;
}

export interface CancelledDealsItem {
  apt_name: string;
  region: string;
  price: number;
  cancel_type: string;
  cancel_day: string;
  deal_date: string;
}

export interface CancelledDealsAnalysis {
  has_data: boolean;
  message?: string;
  stats: CancelledDealsStats;
  by_region: CancelledDealsRegion[];
  by_price_range: CancelledDealsPriceRange[];
  by_month: CancelledDealsMonth[];
  cancelled_items: CancelledDealsItem[];
}

export interface MarketSignal {
  level: 'strong' | 'moderate' | 'weak';
  title: string;
  detail: string;
}

export interface TradeDepthAnalysis {
  dealing_type: DealingTypeAnalysis;
  buyer_seller: BuyerSellerAnalysis;
  cancelled_deals: CancelledDealsAnalysis;
  market_signals: MarketSignal[];
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: string;
  meta?: Record<string, any>;
}

export type EventType = '정책발표' | '금리변동' | '재건축' | '입주시작' | '기타';

export interface EventItem {
  id: string;
  name: string;
  date: string;
  description: string;
  type: EventType;
}

export interface EventImpact {
  event: EventItem;
  before: {
    avg_price: number;
    count: number;
    period_days: number;
  };
  after: {
    avg_price: number;
    count: number;
    period_days: number;
  };
  price_change_pct: number;
  volume_change_pct: number;
  is_significant: boolean;
}
