# Alfred Agent Platform v2 - YouTube Workflow Implementation Plan

## Project Context

The Alfred Agent Platform v2 includes a Social Intelligence Agent with YouTube analysis capabilities, accessible through the Mission Control UI. Two key workflows need to be fully integrated:

1. **Niche-Scout**: Identifies trending YouTube niches based on metrics and trends
2. **Seed-to-Blueprint**: Generates YouTube channel strategies from seed videos or niches

## Current Implementation State

Most components are already implemented but there are integration issues:

- **UI Components**: All workflow pages exist but may have connection issues
- **API Integration**: Endpoints exist but have port configuration problems
- **Social Intelligence Agent**: Running on port 9000, separate from Mission Control (port 3005)

## Primary Issues to Fix

1. **Port Mismatch**: UI runs on port 3005 but API calls target port 3000
2. **API Path Configuration**: Inconsistent paths when calling Social Intelligence Agent
3. **Error Handling**: Needs improvement for better user experience
4. **Documentation**: Requires updates to reflect implementation status

## Implementation Steps

### 1. Fix Port Configuration (Priority High)

```typescript
// Create or update .env.local file
// services/mission-control/.env.local
SOCIAL_INTEL_URL=http://localhost:9000
NEXT_PUBLIC_API_BASE_URL=/api/social-intel
```

```typescript
// Update youtube-workflows.ts service
// Replace static URLs with dynamic detection
const baseUrl = typeof window !== 'undefined' ? window.location.origin : '';
const SOCIAL_INTEL_URL = `${baseUrl}/api/social-intel`;
```

### 2. API Endpoint Improvements (Priority High)

For each API endpoint (`niche-scout.ts`, `seed-to-blueprint.ts`, `workflow-result/[id].ts`):

```typescript
// Update SOCIAL_INTEL_URL constant
const SOCIAL_INTEL_URL = process.env.SOCIAL_INTEL_URL || 'http://localhost:9000';

// Enhance error handling
try {
  // Existing code...
} catch (error) {
  console.error('Detailed error info:', error);
  // Return user-friendly mock data with appropriate structure
}
```

### 3. UI Error Handling Enhancements (Priority Medium)

In all workflow pages (`niche-scout/index.tsx`, `seed-to-blueprint/index.tsx`):

```typescript
// Add improved error state
const [errorDetails, setErrorDetails] = useState<{message: string, technical?: string} | null>(null);

// Enhanced error handling during submission
try {
  // Existing form submission code...
} catch (err) {
  const userMessage = 'We encountered an issue connecting to the Social Intelligence Agent.';
  const technicalDetails = err instanceof Error ? err.message : 'Unknown error';
  setErrorDetails({ message: userMessage, technical: technicalDetails });
  console.error('Workflow error details:', technicalDetails);
}

// In the UI, display appropriate error message
{errorDetails && (
  <div className="error-container">
    <p className="user-error">{errorDetails.message}</p>
    <details>
      <summary>Technical Details</summary>
      <pre>{errorDetails.technical}</pre>
    </details>
  </div>
)}
```

### 4. Dynamic Fallback Mechanism (Priority Medium)

For robust service degradation when the Social Intelligence Agent is unavailable:

```typescript
// Add to youtube-workflows.ts
const useMockData = (error: any): boolean => {
  // Determine if we should use mock data based on error type
  return (
    error instanceof TypeError ||
    (error instanceof Error && error.message.includes('fetch')) ||
    (error instanceof Error && error.message.includes('timeout'))
  );
};

// Use in API handlers
if (useMockData(error)) {
  console.warn('Using mock data due to connection issue');
  return res.status(200).json(getMockData());
}
```

### 5. Update Configuration Files (Priority Medium)

Ensure consistent port configuration:

```json
// In package.json, ensure:
"scripts": {
  "dev": "next dev -p 3005",
  "build": "next build",
  "start": "next start -p 3005",
}
```

```js
// In next.config.js, update or add:
module.exports = {
  reactStrictMode: true,
  env: {
    SOCIAL_INTEL_URL: process.env.SOCIAL_INTEL_URL || 'http://localhost:9000',
  },
  // Additional configuration as needed
}
```

### 6. Testing Steps (Priority High)

1. **Verify API Connectivity:**
   ```bash
   # Test Social Intelligence Agent directly
   curl http://localhost:9000/api/health
   
   # Test proxy endpoint
   curl http://localhost:3005/api/social-intel/workflow-history
   ```

2. **Test UI Workflows:**
   - Run Niche-Scout with sample query "mobile gaming tips"
   - Run Seed-to-Blueprint with sample video URL
   - Check network requests in browser dev tools
   - Verify correct ports and paths in requests

3. **Validate Error Handling:**
   - Test with Social Intelligence Agent stopped
   - Verify mock data is shown
   - Check user-friendly error messages

### 7. Document Implementation Status (Priority Low)

Update `/implementation_status_final.md` with:

- Fixed port configuration issue
- Improved error handling
- Added dynamic fallback mechanism
- Enhanced user feedback
- Updated API integration approach

## Advanced Improvements (If Time Permits)

### 1. Request Caching

```typescript
// Add caching for expensive workflow results
import { useState, useEffect } from 'react';

const useWorkflowCache = <T>(key: string, fetcher: () => Promise<T>, ttl = 3600000) => {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Check cache first
        const cached = localStorage.getItem(`workflow-cache-${key}`);
        if (cached) {
          const { data, timestamp } = JSON.parse(cached);
          if (Date.now() - timestamp < ttl) {
            setData(data);
            setLoading(false);
            return;
          }
        }
        
        // Fetch fresh data
        const result = await fetcher();
        setData(result);
        
        // Cache the result
        localStorage.setItem(`workflow-cache-${key}`, JSON.stringify({
          data: result,
          timestamp: Date.now()
        }));
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Unknown error'));
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [key, fetcher, ttl]);

  return { data, loading, error };
};
```

### 2. Enhance Visualization Options

```tsx
// Add visualization selector to result pages
const [vizType, setVizType] = useState<'scatter' | 'bubble' | 'network'>('scatter');

// Render different visualization based on type
const renderVisualization = () => {
  switch (vizType) {
    case 'scatter':
      return <ScatterPlotChart data={result.trending_niches} />;
    case 'bubble':
      return <BubbleChart data={result.trending_niches} />;
    case 'network':
      return <NetworkGraph data={result.trending_niches} />;
    default:
      return <ScatterPlotChart data={result.trending_niches} />;
  }
};

// Add viz selector in UI
<div className="viz-controls">
  <select 
    value={vizType} 
    onChange={(e) => setVizType(e.target.value as any)}
    className="select-field"
  >
    <option value="scatter">Scatter Plot</option>
    <option value="bubble">Bubble Chart</option>
    <option value="network">Network Graph</option>
  </select>
</div>
```

## Testing Checklist

- [ ] API endpoints resolve to correct ports
- [ ] API proxy correctly forwards to Social Intelligence Agent
- [ ] Error messages are clear and helpful
- [ ] Mock data appears when Social Intelligence Agent is unavailable
- [ ] Both workflows complete successfully with sample inputs
- [ ] Results pages display data correctly
- [ ] Documentation is updated to reflect implementation status

## Next Steps After Implementation

1. Consider adding comprehensive unit tests
2. Explore performance optimizations for large datasets
3. Implement user feedback collection for workflow improvements
4. Add more advanced visualization options