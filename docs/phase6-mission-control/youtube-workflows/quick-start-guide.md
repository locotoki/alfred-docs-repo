# YouTube Workflow Implementation - Quick Start Guide

## Project Overview
The Alfred Agent Platform v2 includes a Social Intelligence Agent with YouTube workflows. The Mission Control UI is being enhanced to interface with these workflows.

## Current Status
- **UI Components**: Both Niche-Scout and Seed-to-Blueprint workflow pages already exist
- **API Integration**: Base endpoints created but need port configuration fixes
- **Primary Issue**: Port mismatch (UI runs on 3005, API endpoints configured for 3000)
- **Social Intelligence Agent**: Running on port 9000

## Key Files & Locations

### UI Pages
- `/services/mission-control/src/pages/workflows/niche-scout/index.tsx`: Niche Scout form
- `/services/mission-control/src/pages/workflows/niche-scout/results/[id].tsx`: Results page
- `/services/mission-control/src/pages/workflows/seed-to-blueprint/index.tsx`: Blueprint form
- `/services/mission-control/src/pages/workflows/seed-to-blueprint/results/[id].tsx`: Results page

### API Endpoints
- `/services/mission-control/src/pages/api/social-intel/niche-scout.ts`: Niche Scout API proxy
- `/services/mission-control/src/pages/api/social-intel/seed-to-blueprint.ts`: Blueprint API proxy
- `/services/mission-control/src/pages/api/social-intel/workflow-history.ts`: Workflow history API
- `/services/mission-control/src/pages/api/social-intel/workflow-result/[id].ts`: Results API

### Services
- `/services/mission-control/src/services/youtube-workflows.ts`: Core service for YouTube API integration

### Types
- `/services/mission-control/src/types/youtube-workflows.ts`: TypeScript types for all workflow entities

## Required Fixes

1. **Port Configuration**
   - Validate that `package.json` has proper port configuration (should use port 3005 for dev and start commands)
   - Ensure `.env.local` contains `SOCIAL_INTEL_URL=http://localhost:9000`

2. **API Integration**
   - Update `SOCIAL_INTEL_URL` in API endpoint files to dynamically detect origin
   - Enhance error handling and timeout management
   - Implement more robust fallback to mock data

3. **UI Improvements**
   - Ensure proper loading states during API calls
   - Add better error handling and user feedback

## Start Debugging Process

1. **Verify Port Configuration**
   ```bash
   cat /services/mission-control/package.json
   # Verify "dev": "next dev -p 3005" and "start": "next start -p 3005"
   
   cat /services/mission-control/next.config.js
   # Check for any port configurations
   
   cat /services/mission-control/.env.local
   # Verify SOCIAL_INTEL_URL=http://localhost:9000
   ```

2. **Update YouTube Workflow Service**
   Key implementation needed:
   ```typescript
   // In youtube-workflows.ts
   // Replace hardcoded URLs with dynamic origin detection
   const baseUrl = typeof window !== 'undefined' ? window.location.origin : '';
   const SOCIAL_INTEL_URL = `${baseUrl}/api/social-intel`;
   ```

3. **Test Workflow Integration**
   - Navigate to `/workflows` page
   - Try running Niche-Scout with a simple query
   - Check browser console for any errors
   - Look at network requests to verify correct port usage

## Additional Notes

- The Social Intelligence Agent container should be running on port 9000
- Mock implementations are already in place for development and testing
- The API proxies have robust error handling with automatic mock data fallbacks
- Mock data mode is automatically activated when the Social Intelligence Agent is unavailable
- All mock data includes an `_id` field which is required for result page navigation
- The system tries multiple endpoint paths to handle different API structures

## Next Steps

1. Test both workflows with actual API integration
2. Monitor network requests to ensure proper routing
3. Enhance error handling for edge cases
4. Update implementation status documentation