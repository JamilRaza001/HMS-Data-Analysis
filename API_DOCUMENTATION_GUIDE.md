# API Documentation Guide for Frontend Teams

## 📋 Table of Contents
1. [Overview](#overview)
2. [Essential Information Checklist](#essential-information-checklist)
3. [Documentation Format](#documentation-format)
4. [Step-by-Step Communication Process](#step-by-step-communication-process)
5. [Example: HMS Analytics API](#example-hms-analytics-api)
6. [Testing Guide for Frontend Teams](#testing-guide-for-frontend-teams)
7. [Common Pitfalls to Avoid](#common-pitfalls-to-avoid)
8. [Additional Resources](#additional-resources)

---

## Overview

This guide provides a standardized approach for backend developers to communicate API endpoint details to frontend teams. Following this format ensures clarity, reduces back-and-forth communication, and accelerates integration.

---

## Essential Information Checklist

When sharing endpoint details, **always include** the following:

### ✅ Core Details
- [ ] **Endpoint URL/Path** - Complete URL or path
- [ ] **HTTP Method** - GET, POST, PUT, DELETE, PATCH, etc.
- [ ] **Authentication** - Required headers, tokens, API keys
- [ ] **Base URL** - Development, staging, and production URLs
- [ ] **API Version** - Version number (e.g., v1, v2)

### ✅ Request Information
- [ ] **Headers** - Required and optional headers
- [ ] **Query Parameters** - Parameters with types, defaults, and constraints
- [ ] **Request Body** - Schema with data types and examples
- [ ] **Content-Type** - (e.g., application/json, multipart/form-data)

### ✅ Response Information
- [ ] **Success Response** - Status code, structure, and example
- [ ] **Error Responses** - All possible error codes with examples
- [ ] **Response Time** - Expected average response time
- [ ] **Pagination** - If applicable, pagination structure

### ✅ Additional Context
- [ ] **Rate Limiting** - Requests per minute/hour limits
- [ ] **CORS Configuration** - Allowed origins
- [ ] **Data Validation Rules** - Field constraints and formats
- [ ] **Sample Code** - Code examples in common languages
- [ ] **Postman Collection** - Pre-configured API testing collection
- [ ] **Changelog** - Version history and breaking changes

---

## Documentation Format

### Template 1: Basic Endpoint Documentation

```markdown
## [Endpoint Name]

**Description:** Brief description of what this endpoint does.

### HTTP Request
`[METHOD] [BASE_URL][PATH]`

### Authentication
- **Type:** Bearer Token / API Key / None
- **Header:** `Authorization: Bearer {token}`

### Request Parameters

#### Headers (Required)
| Header | Type | Required | Description |
|--------|------|----------|-------------|
| Content-Type | string | Yes | application/json |
| Authorization | string | Yes | Bearer token |

#### Query Parameters
| Parameter | Type | Required | Default | Description | Example |
|-----------|------|----------|---------|-------------|---------|
| limit | integer | No | 10 | Number of items per page | 20 |
| offset | integer | No | 0 | Pagination offset | 10 |

#### Request Body
```json
{
  "field_name": "data_type",
  "example_field": "example_value"
}
```

**Field Descriptions:**
- `field_name` (string, required): Description of the field
- `example_field` (string, optional): Description with default value

### Response

#### Success Response (200 OK)
```json
{
  "status": "success",
  "data": {
    "key": "value"
  }
}
```

#### Error Responses

**400 Bad Request**
```json
{
  "status": "error",
  "message": "Invalid request parameters",
  "errors": {
    "field": "Error description"
  }
}
```

**401 Unauthorized**
```json
{
  "status": "error",
  "message": "Authentication required"
}
```

**500 Internal Server Error**
```json
{
  "status": "error",
  "message": "Server error description"
}
```

### Example Usage

#### cURL
```bash
curl -X [METHOD] '[BASE_URL][PATH]' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -d '{
    "key": "value"
  }'
```

#### JavaScript (Fetch)
```javascript
fetch('[BASE_URL][PATH]', {
  method: '[METHOD]',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_TOKEN'
  },
  body: JSON.stringify({
    key: 'value'
  })
})
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

#### Python (Requests)
```python
import requests

url = '[BASE_URL][PATH]'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_TOKEN'
}
payload = {
    'key': 'value'
}

response = requests.[method](url, headers=headers, json=payload)
print(response.json())
```

### Notes
- Additional important information
- Known limitations
- Performance considerations
```

---

## Step-by-Step Communication Process

### Step 1: Prepare Documentation
Create comprehensive documentation using the template above. Include all essential information from the checklist.

### Step 2: Create Postman Collection
1. Create a Postman collection with all endpoints
2. Add example requests with proper authentication
3. Include environment variables for base URLs
4. Export and share the collection JSON file

### Step 3: Schedule Handoff Meeting
1. **Before the meeting:**
   - Send documentation 24-48 hours in advance
   - Share Postman collection
   - Provide test credentials/API keys

2. **During the meeting:**
   - Walk through each endpoint live
   - Demonstrate API calls using Postman
   - Show response structures
   - Explain error handling
   - Answer questions and clarify doubts

3. **After the meeting:**
   - Share meeting notes
   - Provide contact for questions
   - Set up shared Slack/Teams channel

### Step 4: Provide Testing Environment
- **Development Server:** URL and credentials
- **Staging Server:** URL and credentials (if applicable)
- **Test Data:** Sample data or test accounts
- **API Status Dashboard:** Uptime monitoring link (optional)

### Step 5: Ongoing Support
- Create a shared communication channel
- Respond to integration questions within 4 hours
- Update documentation when endpoints change
- Send notifications for breaking changes

---

## Example: HMS Analytics API

Here's how to document the actual HMS Analytics API:

### Endpoint: Get Doctor-Patient Insights

**Description:** Retrieves 20 analytical insights about doctor performance, patient demographics, and clinical trends with visualization-ready data.

### HTTP Request
```
GET https://your-api-domain.vercel.app/api/v1/analytics/doctor-patient-insights
```

**Local Development:**
```
GET http://localhost:8000/api/v1/analytics/doctor-patient-insights
```

### Authentication
- **Type:** None (currently open)
- **Note:** CORS is enabled for all origins (in production, this will be restricted)

### Request Parameters

#### Headers
| Header | Type | Required | Description |
|--------|------|----------|-------------|
| Accept | string | No | application/json (default) |

#### Query Parameters
None

#### Request Body
None - This is a GET request

### Response

#### Success Response (200 OK)

**Response Structure:**
```json
[
  {
    "title": "string",
    "description": "string",
    "chart_type": "bar | pie | line",
    "chart_data": {
      "labels": ["string"],
      "values": [number]
    }
  }
]
```

**Complete Example:**
```json
[
  {
    "title": "Top 5 Busiest Doctors",
    "description": "Doctors with the highest patient volume.",
    "chart_type": "bar",
    "chart_data": {
      "labels": ["Dr. Sarah Johnson", "Dr. Michael Chen", "Dr. Emily Williams", "Dr. James Brown", "Dr. Lisa Anderson"],
      "values": [87, 82, 78, 75, 71]
    }
  },
  {
    "title": "Patient Visits by Department",
    "description": "Distribution of cases across different medical departments.",
    "chart_type": "pie",
    "chart_data": {
      "labels": ["Cardiology", "Orthopedics", "Pediatrics", "Neurology", "Emergency"],
      "values": [234, 198, 187, 156, 142]
    }
  }
]
```

**Response Fields:**
- `title` (string): Display title for the chart
- `description` (string): Explanation of what the insight shows
- `chart_type` (string): Type of visualization - "bar", "pie", or "line"
- `chart_data` (object): Contains the data for visualization
  - `labels` (array of strings): X-axis labels or category names
  - `values` (array of numbers): Corresponding numeric values

**Total Insights:** The response always contains exactly **20 insights** covering:
1. **Doctor Performance** (Insights 1-4)
2. **Patient Demographics** (Insights 5-7)
3. **Clinical Demand & Trends** (Insights 8-20)

#### Error Response (500 Internal Server Error)

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Chart Types Guide

| chart_type | Best Use Case | Frontend Implementation |
|------------|---------------|------------------------|
| `bar` | Comparing quantities across categories | Bar chart, horizontal bar chart |
| `pie` | Showing proportions of a whole | Pie chart, donut chart |
| `line` | Displaying trends over time | Line chart, area chart |

### Example Usage

#### cURL
```bash
curl -X GET 'https://your-api-domain.vercel.app/api/v1/analytics/doctor-patient-insights' \
  -H 'Accept: application/json'
```

#### JavaScript (Fetch)
```javascript
const fetchInsights = async () => {
  try {
    const response = await fetch('https://your-api-domain.vercel.app/api/v1/analytics/doctor-patient-insights');
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const insights = await response.json();
    
    // Process insights
    insights.forEach(insight => {
      console.log(`${insight.title}: ${insight.chart_type} chart`);
      console.log(`Labels: ${insight.chart_data.labels}`);
      console.log(`Values: ${insight.chart_data.values}`);
    });
    
    return insights;
  } catch (error) {
    console.error('Error fetching insights:', error);
  }
};

fetchInsights();
```

#### JavaScript (Axios)
```javascript
import axios from 'axios';

const API_BASE_URL = 'https://your-api-domain.vercel.app/api/v1';

const getInsights = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/analytics/doctor-patient-insights`);
    return response.data;
  } catch (error) {
    if (error.response) {
      console.error('Server Error:', error.response.status, error.response.data);
    } else if (error.request) {
      console.error('Network Error:', error.request);
    } else {
      console.error('Error:', error.message);
    }
    throw error;
  }
};
```

#### Python (Requests)
```python
import requests

API_BASE_URL = 'https://your-api-domain.vercel.app/api/v1'

def get_insights():
    try:
        response = requests.get(f'{API_BASE_URL}/analytics/doctor-patient-insights')
        response.raise_for_status()
        
        insights = response.json()
        
        for insight in insights:
            print(f"Title: {insight['title']}")
            print(f"Chart Type: {insight['chart_type']}")
            print(f"Labels: {insight['chart_data']['labels']}")
            print(f"Values: {insight['chart_data']['values']}")
            print('-' * 50)
        
        return insights
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

insights = get_insights()
```

#### React Example (Complete Component)
```javascript
import React, { useState, useEffect } from 'react';

const API_BASE_URL = 'https://your-api-domain.vercel.app/api/v1';

function InsightsDashboard() {
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchInsights = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${API_BASE_URL}/analytics/doctor-patient-insights`);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        setInsights(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchInsights();
  }, []);

  if (loading) return <div>Loading insights...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="dashboard">
      <h1>HMS Analytics Dashboard</h1>
      {insights.map((insight, index) => (
        <div key={index} className="insight-card">
          <h3>{insight.title}</h3>
          <p>{insight.description}</p>
          <div>Chart Type: {insight.chart_type}</div>
          {/* Render your chart here using insight.chart_data */}
        </div>
      ))}
    </div>
  );
}

export default InsightsDashboard;
```

### Frontend Integration Checklist

**For React (or similar frameworks):**
- [ ] Install chart library (e.g., `recharts`, `chart.js`, `victory`)
- [ ] Create API service file for endpoint calls
- [ ] Implement error boundary for API failures
- [ ] Add loading states during data fetch
- [ ] Handle empty/null data scenarios
- [ ] Implement retry logic for failed requests
- [ ] Add environment variables for API URLs

**For Streamlit:**
- [ ] Use `requests` library for API calls
- [ ] Implement caching with `@st.cache_data`
- [ ] Map chart types to Streamlit chart components
- [ ] Handle connection errors gracefully
- [ ] Add refresh button for manual updates

### Performance Considerations

- **Response Time:** Typically 200-500ms for full dataset
- **Data Size:** Approximately 5-10 KB per response
- **Caching:** Consider caching on frontend (5-10 minute TTL)
- **Refresh Rate:** Recommend polling every 30-60 seconds max

### Known Limitations

- Response always returns 20 insights (fixed number)
- No filtering or pagination available
- No real-time updates (requires polling)
- Rate limiting not currently implemented

### Troubleshooting

**Issue:** CORS Error
- **Cause:** Frontend domain not whitelisted
- **Solution:** Contact backend team to add domain to `allow_origins`

**Issue:** 500 Error
- **Cause:** Data file missing or corrupted
- **Solution:** Backend needs to regenerate mock data

**Issue:** Empty labels/values arrays
- **Cause:** Insufficient data for specific insight
- **Solution:** Check data integrity or skip visualization

---

## Testing Guide for Frontend Teams

### Step 1: Test with cURL
```bash
# Test basic connectivity
curl https://your-api-domain.vercel.app/api/v1/analytics/doctor-patient-insights

# Pretty print JSON
curl https://your-api-domain.vercel.app/api/v1/analytics/doctor-patient-insights | json_pp
```

### Step 2: Import Postman Collection
1. Download the Postman collection (provided separately)
2. Import into Postman
3. Set environment variables:
   - `base_url_dev`: `http://localhost:8000`
   - `base_url_prod`: `https://your-api-domain.vercel.app`
4. Run the collection

### Step 3: Test Error Scenarios
```javascript
// Test timeout handling
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 5000);

fetch(API_URL, { signal: controller.signal })
  .then(response => {
    clearTimeout(timeoutId);
    return response.json();
  })
  .catch(error => {
    if (error.name === 'AbortError') {
      console.log('Request timeout');
    }
  });

// Test network error
fetch('http://invalid-url.com')
  .catch(error => console.log('Network error:', error));

// Test malformed response
fetch(API_URL)
  .then(response => response.json())
  .catch(error => console.log('JSON parse error:', error));
```

### Step 4: Validate Response Structure
```javascript
const validateInsight = (insight) => {
  const required = ['title', 'description', 'chart_type', 'chart_data'];
  const hasAllFields = required.every(field => field in insight);
  
  const validChartTypes = ['bar', 'pie', 'line'];
  const hasValidChartType = validChartTypes.includes(insight.chart_type);
  
  const hasLabelsAndValues = 
    Array.isArray(insight.chart_data.labels) &&
    Array.isArray(insight.chart_data.values) &&
    insight.chart_data.labels.length === insight.chart_data.values.length;
  
  return hasAllFields && hasValidChartType && hasLabelsAndValues;
};

// Use in your code
fetch(API_URL)
  .then(response => response.json())
  .then(insights => {
    insights.forEach((insight, index) => {
      if (!validateInsight(insight)) {
        console.error(`Invalid insight at index ${index}:`, insight);
      }
    });
  });
```

---

## Common Pitfalls to Avoid

### ❌ Don't Do This:

1. **Vague endpoint descriptions**
   - ❌ "This endpoint gets data"
   - ✅ "Retrieves 20 analytical insights about doctor performance, patient demographics, and clinical trends"

2. **Missing base URL**
   - ❌ "/api/v1/analytics/insights"
   - ✅ "GET https://api.example.com/api/v1/analytics/insights"

3. **No error examples**
   - ❌ "Returns 500 on error"
   - ✅ Provide actual error response JSON with all possible error codes

4. **Unclear data types**
   - ❌ "Send user data"
   - ✅ 
   ```json
   {
     "user_id": 123,           // integer, required
     "username": "john_doe",   // string, required, max 50 chars
     "email": "user@mail.com"  // string, required, valid email format
   }
   ```

5. **No code examples**
   - ❌ Just showing curl command
   - ✅ Provide examples in JavaScript, Python, and curl

6. **Forgetting authentication details**
   - ❌ "Use token"
   - ✅ "Add header: `Authorization: Bearer YOUR_ACCESS_TOKEN`"

7. **Not documenting edge cases**
   - ❌ Only showing happy path
   - ✅ Document what happens with empty data, invalid input, timeout, etc.

---

## Additional Resources

### Tools for API Documentation

1. **Swagger/OpenAPI**
   - Auto-generate interactive documentation
   - Install: `pip install fastapi[all]` (includes Swagger UI)
   - Access at: `http://localhost:8000/docs`

2. **Postman**
   - Create and share API collections
   - Auto-generate documentation
   - Website: https://www.postman.com

3. **Stoplight**
   - Visual API designer
   - Collaborative documentation
   - Website: https://stoplight.io

4. **ReadMe.io**
   - Beautiful API documentation hosting
   - Interactive code examples
   - Website: https://readme.com

### Communication Templates

#### Email Template
```
Subject: API Endpoint Documentation - [Feature Name]

Hi [Frontend Team],

I've prepared the API documentation for [feature/module name]. Please find the details below:

📄 Documentation: [Link to documentation]
🧪 Postman Collection: [Attached/Link]
🔑 Test Credentials: [Provided separately for security]
🌐 Base URLs:
  - Development: http://localhost:8000
  - Staging: https://staging.example.com
  - Production: https://api.example.com

Key Points:
- [Important point 1]
- [Important point 2]
- [Important point 3]

Let's schedule a 30-minute walkthrough session. Available times:
- [Option 1]
- [Option 2]
- [Option 3]

Contact me if you have any questions!

Best regards,
[Your Name]
```

#### Slack/Teams Message Template
```
🚀 New API Endpoint Ready for Integration

**Endpoint:** GET /api/v1/analytics/doctor-patient-insights
**Documentation:** [Link]
**Status:** ✅ Ready for integration
**Environment:** Dev, Staging, Production

Quick summary:
• Returns 20 analytics insights
• No authentication required (for now)
• Response format: JSON array
• Avg response time: 300ms

📎 Postman collection attached
📅 Walkthrough session: [Date/Time]

Questions? Thread below 👇
```

### Documentation Best Practices

1. **Keep it Updated**
   - Update documentation immediately when endpoints change
   - Version your API and documentation together
   - Maintain a changelog

2. **Make it Searchable**
   - Use clear headings and structure
   - Add a table of contents
   - Include keywords for search

3. **Be Consistent**
   - Use the same format for all endpoints
   - Maintain consistent naming conventions
   - Use a style guide

4. **Include Visual Aids**
   - Add diagrams for complex workflows
   - Show request/response flow
   - Use screenshots for UI-related endpoints

5. **Provide Context**
   - Explain business logic when relevant
   - Document why certain fields are required
   - Explain data relationships

---

## Quick Reference Checklist

When sharing endpoint details, use this checklist:

```markdown
## [ENDPOINT_NAME]

- [ ] HTTP Method documented
- [ ] Full URL with base URL provided
- [ ] Authentication requirements explained
- [ ] All headers documented (required + optional)
- [ ] Query parameters with types and defaults
- [ ] Request body schema with examples
- [ ] Success response with example
- [ ] All error responses documented
- [ ] Code examples in 3+ languages
- [ ] cURL command provided
- [ ] Postman collection created
- [ ] Expected response time mentioned
- [ ] Known limitations documented
- [ ] Frontend integration examples provided
- [ ] Testing guide included
- [ ] Contact person for support listed
```

---

## Summary

**The Golden Rule:** *Document as if the frontend team has no prior knowledge of your system.*

**Key Takeaways:**
1. ✅ Always provide complete, working examples
2. ✅ Include all possible error scenarios
3. ✅ Offer code in multiple languages
4. ✅ Schedule a live walkthrough
5. ✅ Remain available for questions during integration
6. ✅ Keep documentation updated as APIs evolve

**Remember:** Good API documentation is not just about technical accuracy—it's about enabling other teams to integrate quickly and confidently!

---

**Document Version:** 1.0  
**Last Updated:** 2025-12-01  
**Contact:** [Your Name/Team]  
**Support Channel:** [Slack/Teams/Email]
