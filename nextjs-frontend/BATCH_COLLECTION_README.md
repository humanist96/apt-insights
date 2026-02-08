# Batch Collection Admin Page

## Overview
The Batch Collection admin page allows administrators to collect apartment real estate transaction data from multiple regions and date ranges in bulk through the Korean Ministry of Land public data APIs.

## Access
- **URL**: http://localhost:3000/admin/batch-collection
- **Authentication**: Password-protected (Demo password: `admin123`)
- **Note**: Authentication state is stored in `localStorage`

## Features

### 1. Admin Authentication
- Simple password-based authentication
- Mock authentication system (production should use proper auth)
- Session persistence using localStorage
- Logout functionality

### 2. Collection Configuration
- **Region Selection**:
  - Multiple region selection with checkboxes
  - Select all / Deselect all functionality
  - Includes major regions: Seoul districts and Suwon districts

- **Date Range**:
  - Month-based date picker
  - Start month and end month selection
  - Validates that start month <= end month

- **API Selection**:
  - API 01: Pre-sale Rights (분양권전매)
  - API 02: Apartment Trade (매매)
  - API 03: Detailed Trade (매매 상세)
  - API 04: Rental (전월세)

### 3. Collection Progress Display
- **Real-time Progress**:
  - Overall progress bar with percentage
  - Individual API progress bars
  - Current month being processed
  - Success/error/total record counts

- **Status Information**:
  - Start time and end time
  - Elapsed time
  - Estimated completion time
  - Current status badges

- **Cancel Functionality**:
  - Cancel button to stop collection mid-process
  - Status updates to "cancelled"

### 4. Collection History
- **Table View**:
  - Collection timestamp
  - Regions collected
  - APIs used
  - Total records collected
  - Success/failure counts
  - Duration
  - Status badges

- **Detail Modal**:
  - View full details of past collections
  - Configuration used
  - Complete statistics
  - Error messages (if any)

### 5. Statistics Dashboard
- Total collections performed
- Successful collections
- Failed collections
- Total records collected across all collections

## File Structure

```
app/admin/batch-collection/
  └── page.tsx                    # Main admin page component

components/admin/
  ├── CollectionConfig.tsx        # Configuration form component
  ├── CollectionProgress.tsx      # Progress display component
  └── CollectionHistory.tsx       # History table and detail modal

hooks/
  └── useBatchCollection.ts       # Collection logic and state management

types/
  └── batch-collection.ts         # TypeScript type definitions

lib/
  └── batch-collection-mock.ts    # Mock data and helper functions
```

## Component Details

### CollectionConfig
- Validates user input (at least 1 region, 1 API selected)
- Disabled state during active collection
- Real-time validation feedback
- Month range picker with min/max bounds

### CollectionProgress
- Displays overall and per-API progress
- Auto-updates during collection (simulated with setTimeout)
- Shows success/error counts
- Calculates and displays duration
- Cancel button (only shown during active collection)

### CollectionHistory
- Paginated table view (currently shows all)
- Detail modal with full information
- Status badges for visual clarity
- Empty state handling

### useBatchCollection Hook
- `startCollection(config)`: Starts data collection process
- `cancelCollection()`: Cancels active collection
- `getCollectionHistory()`: Retrieves collection history from localStorage
- `isCollecting`: Boolean flag for collection state
- `progress`: Current collection progress object

## Data Flow

1. User configures collection settings (regions, dates, APIs)
2. Configuration validated in real-time
3. User clicks "Start Collection" button
4. Hook initiates collection process with simulated API calls
5. Progress updates every 100ms (mock delay)
6. Success/error counts tracked per API
7. Results saved to collection history in localStorage
8. History table updates with new entry

## Mock Implementation

Currently uses mock data and simulated API calls:
- Progress updates: 100ms delay per API call
- Random success rate: ~95% (5% failure rate)
- Random record counts: 50-550 per successful call
- Collection history stored in localStorage

## Production Considerations

### To Replace for Production:

1. **Authentication**:
   - Replace mock auth with proper JWT/session-based auth
   - Add user roles and permissions
   - Implement secure password hashing

2. **API Integration**:
   - Replace simulated API calls with actual API endpoints
   - Implement proper error handling and retries
   - Add rate limiting to respect API quotas

3. **Data Storage**:
   - Replace localStorage with database storage
   - Track collection metadata in backend
   - Store collected data in PostgreSQL

4. **Real-time Updates**:
   - Replace setTimeout simulation with WebSocket or Server-Sent Events
   - Stream progress updates from backend
   - Handle disconnections and reconnections

5. **Error Handling**:
   - Detailed error logging
   - Retry logic for failed requests
   - Email notifications for failures
   - Automatic recovery mechanisms

6. **Performance**:
   - Implement background job processing (Celery, BullMQ)
   - Add queue management
   - Parallel processing for multiple regions
   - Progress tracking in Redis

## Testing

To test the batch collection page:

```bash
# Start development server
npm run dev

# Navigate to
http://localhost:3000/admin/batch-collection

# Login with demo password
admin123

# Configure collection and start
```

## Known Limitations

- Mock data only (not connected to real APIs)
- No actual data collection or storage
- Simple password authentication (insecure for production)
- Progress simulation (not real API calls)
- localStorage-based history (not persistent across sessions/devices)
- No pagination in history table
- No export functionality for collected data

## Future Enhancements

- [ ] Real API integration
- [ ] Database-backed collection history
- [ ] User authentication and authorization
- [ ] Collection scheduling (cron jobs)
- [ ] Email notifications for completion/failures
- [ ] Export collected data (CSV, Excel)
- [ ] Advanced filtering in history table
- [ ] Collection templates (save common configurations)
- [ ] Bulk delete/retry for failed collections
- [ ] API usage statistics and quota tracking
